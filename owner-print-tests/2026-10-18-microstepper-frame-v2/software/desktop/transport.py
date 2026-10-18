"""USB serial framing and actual-firmware simulation, owned by one I/O worker."""
import importlib.util
import json
import threading
import time
from pathlib import Path


class CommandError(Exception):
    pass


class StopRequested(Exception):
    pass


def ports():
    try:
        from serial.tools import list_ports
        return [{"device": item.device, "description": item.description, "serial_number": item.serial_number}
                for item in list_ports.comports()]
    except ImportError:
        return []


class SerialLink:
    simulated = False

    def __init__(self, port, stop_event=None, timeout=1.2, serial_factory=None):
        if serial_factory is None:
            import serial
            serial_factory = serial.Serial
        self.serial = serial_factory(port, baudrate=115200, timeout=0.02, write_timeout=0.2)
        self.stop_event = stop_event or threading.Event()
        self.timeout = timeout
        self.counter = 0
        self.buffer = bytearray()
        self.stats = {"requests": 0, "responses": 0, "timeouts": 0, "invalid_lines": 0}

    def request(self, request):
        if self.stop_event.is_set():
            self.emergency_stop()
            raise StopRequested("STOP vóór serieel verzoek")
        self.counter += 1
        message = dict(request, id=self.counter)
        packet = (json.dumps(message, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        if len(packet) > 8192:
            raise CommandError("Commando overschrijdt 8192 bytes")
        self.serial.write(packet)
        self.stats["requests"] += 1
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            if self.stop_event.is_set():
                self.emergency_stop()
                raise StopRequested("STOP tijdens serieel verzoek")
            self.buffer.extend(self.serial.read(4096))
            if len(self.buffer) > 65536:
                self.buffer.clear()
                raise OSError("Te lang serieel antwoord")
            while b"\n" in self.buffer:
                line, _, remaining = self.buffer.partition(b"\n")
                self.buffer = bytearray(remaining)
                try:
                    response = json.loads(line.decode("utf-8"))
                except (ValueError, UnicodeError):
                    self.stats["invalid_lines"] += 1
                    continue
                if not isinstance(response, dict) or response.get("id") != self.counter:
                    continue
                self.stats["responses"] += 1
                if not response.get("ok"):
                    raise CommandError(response.get("error", "Onbekende firmwarefout"))
                return response.get("result", {})
        self.stats["timeouts"] += 1
        raise OSError("Geen Pico-antwoord binnen %.1f s; beweging niet hervatten" % self.timeout)

    def tick(self):
        pass

    def emergency_stop(self):
        self.serial.write(b"!")
        # A request interrupted by ! can leave a response with its old id; framing ignores it.

    def close(self):
        self.serial.close()


class SimulatedLink:
    simulated = True

    def __init__(self, firmware=None):
        if firmware is None:
            path = Path(__file__).resolve().parents[1] / "main.py"
            spec = importlib.util.spec_from_file_location("e302_simulated_firmware", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            firmware = module.make_simulated_firmware()
        self.firmware = firmware
        self.counter = 0
        self.stats = {"requests": 0, "responses": 0, "timeouts": 0, "invalid_lines": 0}

    def request(self, request):
        self.tick()
        self.counter += 1
        # Roundtrip serial encoding also catches non-JSON and nonfinite input in simulation.
        message = json.loads(json.dumps(dict(request, id=self.counter), allow_nan=False))
        response = json.loads(json.dumps(self.firmware.handle(message), allow_nan=False))
        self.stats["requests"] += 1
        self.stats["responses"] += 1
        if not response.get("ok"):
            raise CommandError(response.get("error", "Simulatiefout"))
        return response.get("result", {})

    def tick(self):
        self.firmware.tick(time.monotonic())

    def emergency_stop(self):
        self.firmware.emergency_stop()

    def close(self):
        self.emergency_stop()
