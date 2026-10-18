"""Profiles, experiment steps and measurement provenance; no hardware dependencies."""
import csv
import itertools
import json
import math
import uuid
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def finite_positive(value, name):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(name + " moet eindig en positief zijn")
    return number


def calibration_factor(previous, calculated_rev, measured_rev=None,
                       measured_mm=None, lead_mm_per_rev=None):
    """Observed / already-calibrated prediction, composed with previous factor."""
    calculated = finite_positive(abs(float(calculated_rev)), "Berekende omwentelingen")
    if (measured_rev is None) == (measured_mm is None):
        raise ValueError("Vul precies één meting in: omwentelingen of verplaatsing")
    if measured_rev is not None:
        observed = finite_positive(abs(float(measured_rev)), "Gemeten omwentelingen")
    else:
        observed = finite_positive(abs(float(measured_mm)), "Gemeten verplaatsing") / finite_positive(lead_mm_per_rev, "Spoed")
    return finite_positive(previous, "Bestaande factor") * observed / calculated


def rpm_values(start, end, step):
    start, end, step = float(start), float(end), float(step)
    if not all(math.isfinite(n) for n in (start, end, step)) or step == 0:
        raise ValueError("RPM-bereik en stap moeten eindig zijn; stap mag niet nul zijn")
    if (end - start) * step < 0:
        raise ValueError("RPM-stap wijst van de eindwaarde weg")
    count = int(math.floor((end - start) / step + 1e-10)) + 1
    for index in range(count):
        yield start + index * step


def comparison_steps(base_move, rpms, accelerations, choppers, microsteps, currents):
    """Lazy Cartesian sweep; individual commands still validated by firmware."""
    pools = tuple(tuple(values) for values in (accelerations, choppers, microsteps, currents))
    for rpm in rpms:
        for accel, chopper, microstep, current in itertools.product(*pools):
            move = dict(base_move, rpm=float(rpm), accel=float(accel))
            if move.get("mode") == "continuous":
                raise ValueError("Automatische tests vereisen een eindige beweging")
            yield {"config": {"chopper": chopper, "microsteps": int(microstep), "irun": int(current),
                               "tpowerdown": 20 if chopper == "stealthchop" else 0},
                   "move": move}


class Results:
    """Blank measurements stay absent; calculated telemetry is never a measurement."""
    def __init__(self):
        self.records = []

    def begin(self, motor, requested, config, simulated=False):
        record = {"test_id": str(uuid.uuid4()), "started_utc": utc_now(),
                  "source": "simulated" if simulated else "hardware_session",
                  "motor": motor, "requested": requested.copy(), "configured": config.copy(),
                  "calculated": {}, "manual_measurements": {}, "observations": {},
                  "diagnostics": {}, "uart": {}, "outcome": "running", "samples": []}
        self.records.append(record)
        return record

    def sample(self, record, status):
        sample = {"utc": utc_now(), "calculated": status.get("motion", {}).copy(),
                  "diagnostics": status.get("diagnostics", {}).copy(), "uart": status.get("uart", {}).copy()}
        record["samples"].append(sample)
        record["calculated"] = sample["calculated"]
        record["diagnostics"] = sample["diagnostics"]
        record["uart"] = sample["uart"]
        record["fault"] = status.get("fault")

    def finish(self, record, outcome, error=None):
        record["finished_utc"] = utc_now()
        record["outcome"] = outcome
        if error:
            record["error"] = str(error)

    def measure(self, record, values, method, observation="", provenance="manual_measurement"):
        if provenance not in ("manual_measurement", "instrument_measurement"):
            raise ValueError("Kies handmatige of instrumentele meting")
        allowed = {"displacement_mm", "revolutions", "rpm", "load_g", "vref_v", "vm_v", "motor_temperature_c"}
        entered = {key: float(value) for key, value in values.items() if value not in (None, "")}
        if set(entered) - allowed or not all(math.isfinite(v) for v in entered.values()):
            raise ValueError("Onbekende of niet-eindige meetwaarde")
        if entered and not method.strip():
            raise ValueError("Vermeld meetmethode/instrument; een waarneming is geen meting")
        for key, value in entered.items():
            record["manual_measurements"][key] = {"value": value, "provenance": provenance,
                                                   "method": method.strip(), "entered_utc": utc_now()}
        if observation.strip():
            record["observations"]["notes"] = {"text": observation.strip(), "provenance": "manual_observation"}

    def export_json(self, path):
        Path(path).write_text(json.dumps({"format": "e302-results-v1", "exported_utc": utc_now(),
                                         "records": self.records}, indent=2, allow_nan=False), encoding="utf-8")

    def export_csv(self, path):
        # JSON columns retain nested settings, provenance, diagnostics and every sample.
        fields = ["test_id", "started_utc", "finished_utc", "source", "motor", "outcome", "error",
                  "requested", "configured", "calculated", "manual_measurements", "observations", "diagnostics", "uart", "samples"]
        with open(path, "w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for record in self.records:
                writer.writerow({key: json.dumps(record[key], ensure_ascii=False, allow_nan=False)
                                 if isinstance(record.get(key), (dict, list)) else record.get(key, "") for key in fields})


def save_profile(path, profile):
    Path(path).write_text(json.dumps({"format": "e302-profile-v1", "profile": profile}, indent=2,
                                    allow_nan=False), encoding="utf-8")


def load_profile(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("format") != "e302-profile-v1" or not isinstance(data.get("profile"), dict):
        raise ValueError("Geen E-302-profiel")
    return data["profile"]
