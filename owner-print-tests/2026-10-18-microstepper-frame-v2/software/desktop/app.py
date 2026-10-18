"""Tkinter control panel. All serial I/O and sweep progression run off the Tk thread."""
import argparse
import json
import queue
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from .model import calibration_factor, comparison_steps, load_profile, rpm_values, save_profile
from .worker import SessionWorker


class Application:
    def __init__(self, root, simulate=False):
        self.root = root
        self.root.title("E-302 · Microstepper testbank")
        self.root.geometry("1060x850")
        self.root.minsize(790, 600)
        self.worker = SessionWorker()
        self.pending = []
        self.statuses = {}
        self.profiles = {}
        self.schema = {}
        self.last_record_ids = set()
        self.closing = False
        self.port = tk.StringVar(value="SIMULATIE" if simulate else "")
        self.motor = tk.StringVar(value="m1")
        self.connection = tk.StringVar(value="Niet verbonden")
        self.summary = tk.StringVar(value="Berekende beweging; geen positie- of RPM-sensor")
        self.notice = tk.StringVar(value="Fysieke motorvoedingsschakelaar bereikbaar houden.")
        self.reconnect = tk.BooleanVar(value=True)
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        self.port_box = ttk.Combobox(top, textvariable=self.port, width=20)
        self.port_box.pack(side="left")
        ttk.Button(top, text="Verbinden", command=self.connect).pack(side="left", padx=4)
        ttk.Button(top, text="Verbreken", command=lambda: self.send("_disconnect")).pack(side="left")
        ttk.Checkbutton(top, text="Opnieuw verbinden", variable=self.reconnect).pack(side="left", padx=5)
        self.motor_box = ttk.Combobox(top, textvariable=self.motor, values=["m1"], state="readonly", width=8)
        self.motor_box.pack(side="left", padx=5)
        self.motor_box.bind("<<ComboboxSelected>>", lambda event: self.select_motor())
        tk.Button(top, text="STOP · ALLE MOTOREN", bg="#bc2025", fg="white", activebackground="#e23d3d",
                  font=("Arial", 13, "bold"), command=self.stop).pack(side="right", padx=4)
        ttk.Label(root, textvariable=self.connection, padding=(10, 2)).pack(anchor="w")
        ttk.Label(root, textvariable=self.summary, padding=(10, 2), wraplength=1000).pack(anchor="w")
        ttk.Label(root, textvariable=self.notice, foreground="#9b3918", padding=(10, 4), wraplength=1000).pack(anchor="w")
        book = ttk.Notebook(root)
        book.pack(fill="both", expand=True, padx=8, pady=4)
        self.tabs = {}
        for title in ("Beweging", "Motor / driver", "Pintest", "Automatische tests", "Resultaten", "Diagnostiek"):
            frame = ttk.Frame(book, padding=10)
            book.add(frame, text=title)
            self.tabs[title] = frame
        self.make_motion()
        self.make_driver()
        self.make_mechanics()
        self.make_automation()
        self.make_results()
        self.make_diagnostics()
        footer = ttk.Frame(root, padding=8)
        footer.pack(fill="x")
        ttk.Button(footer, text="Instellingen/profiel opslaan…", command=self.save).pack(side="left")
        ttk.Button(footer, text="Profiel laden…", command=self.load).pack(side="left", padx=5)
        ttk.Label(footer, text="Esc = STOP · herstel hervat nooit een test").pack(side="right")
        root.bind_all("<Escape>", lambda event: self.stop())
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.worker.start()
        self.root.after(50, self.pump)
        if simulate:
            self.connect()

    def entry(self, parent, row, label, variable, values=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4, padx=4)
        widget = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly") if values else ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row, column=1, sticky="ew", padx=4, pady=4)
        parent.columnconfigure(1, weight=1)
        return widget

    def guarded(self, action):
        try:
            return action()
        except Exception as exc:
            self.notice.set(str(exc))
            return None

    def send(self, command, callback=None, **parameters):
        future = self.worker.submit(command, **parameters)
        self.pending.append((future, callback))
        return future

    def connect(self):
        if not self.port.get():
            self.notice.set("Selecteer een COM-poort of SIMULATIE")
            return
        self.send("_connect", port=self.port.get(), reconnect=self.reconnect.get())

    def stop(self):
        self.worker.stop_now()
        self.notice.set("STOP aangevraagd. Bij twijfel motorvoeding fysiek uitschakelen.")

    def make_motion(self):
        f = self.tabs["Beweging"]
        self.move_vars = {name: tk.StringVar(value=value) for name, value in {
            "mode": "continuous", "rpm": "30", "accel": "100", "decel": "100", "revolutions": "1",
            "duration_s": "5", "cycles": "3", "dwell_s": "0.3"}.items()}
        labels = {"mode": "Testvorm", "rpm": "Doel-RPM (teken = richting)", "accel": "Acceleratie (RPM/s)",
                  "decel": "Deceleratie (RPM/s)", "revolutions": "Omwentelingen per beweging / cyclushelft",
                  "duration_s": "Duur (s)", "cycles": "Aantal op/neercycli", "dwell_s": "Pauze bij cyclusomkeer (s)"}
        for row, (key, var) in enumerate(self.move_vars.items()):
            self.entry(f, row, labels[key], var, ["continuous", "revolutions", "duration", "cycles"] if key == "mode" else None)
        buttons = ttk.Frame(f)
        buttons.grid(row=8, column=0, columnspan=2, sticky="w", pady=14)
        ttk.Button(buttons, text="Start motor", command=lambda: self.guarded(self.start_move)).pack(side="left", padx=4)
        ttk.Button(buttons, text="RPM live toepassen", command=lambda: self.guarded(self.change_speed)).pack(side="left", padx=4)
        ttk.Button(buttons, text="Richting wisselen", command=lambda: self.guarded(self.reverse)).pack(side="left", padx=4)
        ttk.Button(buttons, text="Gecontroleerd stoppen", command=lambda: self.send("stop", motor=self.motor.get())).pack(side="left", padx=4)
        ttk.Label(f, text="Start controleert de driver automatisch. Live RPM en omkeren werken tijdens vrij continu draaien.\n"
                  "Een cyclus beweegt het gekozen aantal omwentelingen heen én terug.\n"
                  "Hoge ingestelde RPM bewijst geen echte snelheid of beschikbaar koppel.", wraplength=850).grid(row=9, column=0, columnspan=2, sticky="w")

    def move_request(self):
        result = {"mode": self.move_vars["mode"].get()}
        for key in ("rpm", "accel", "decel"):
            result[key] = float(self.move_vars[key].get())
        if result["mode"] in ("revolutions", "cycles"):
            result["revolutions"] = float(self.move_vars["revolutions"].get())
        if result["mode"] == "duration":
            result["duration_s"] = float(self.move_vars["duration_s"].get())
        if result["mode"] == "cycles":
            result["cycles"] = int(self.move_vars["cycles"].get())
            result["dwell_s"] = float(self.move_vars["dwell_s"].get())
        return result

    def start_move(self):
        self.send("move", motor=self.motor.get(), **self.move_request())

    def change_speed(self):
        self.send("speed", motor=self.motor.get(), **{key: float(self.move_vars[key].get()) for key in ("rpm", "accel", "decel")})

    def reverse(self):
        self.move_vars["rpm"].set(str(-float(self.move_vars["rpm"].get())))
        if self.statuses.get(self.motor.get(), {}).get("state") in ("running", "warming"):
            self.change_speed()

    def make_driver(self):
        f = self.tabs["Motor / driver"]
        top = ttk.Frame(f)
        top.pack(fill="x")
        self.driver_profile = tk.StringVar()
        self.profile_box = ttk.Combobox(top, textvariable=self.driver_profile, state="readonly", width=28)
        self.profile_box.pack(side="left")
        ttk.Button(top, text="Standaardprofiel in editor", command=self.load_driver_profile).pack(side="left", padx=5)
        ttk.Button(top, text="Huidige instellingen ophalen", command=self.get_driver_config).pack(side="left", padx=5)
        basic = ttk.LabelFrame(f, text="Basisinstellingen", padding=5)
        basic.pack(fill="x", pady=7)
        specs = [("chopper", "Chopper", "spreadcycle", ["spreadcycle", "stealthchop"]),
                 ("microsteps", "Microstappen", "8", [1, 2, 4, 8, 16, 32, 64, 128, 256]),
                 ("full_steps_per_rev", "Volle stappen / omw", "20", None),
                 ("irun", "IRUN (0–31)", "5", None), ("ihold", "IHOLD (0–31)", "5", None),
                 ("vref_v", "Vref gemeten (V)", "0.8", None)]
        self.basic_vars = {}
        for index, (key, label, default, values) in enumerate(specs):
            var = self.basic_vars[key] = tk.StringVar(value=default)
            row, column = index // 2, (index % 2) * 2
            ttk.Label(basic, text=label).grid(row=row, column=column, sticky="w", padx=4, pady=3)
            widget = ttk.Combobox(basic, textvariable=var, values=values, state="readonly", width=16) if values else ttk.Entry(basic, textvariable=var, width=18)
            widget.grid(row=row, column=column + 1, sticky="ew", padx=4, pady=3)
            basic.columnconfigure(column + 1, weight=1)
        ttk.Button(basic, text="Basisinstellingen toepassen", command=lambda: self.guarded(self.apply_basic)).grid(row=3, column=0, columnspan=4, sticky="w", pady=5)
        ttk.Label(f, text="Vref is handmatige invoer; UART kan Vref niet meten of instellen. Wijzig instellingen bij stilstand.\n"
                  "Geavanceerd: alle driverinstellingen als JSON; aparte toepassing van deze editor.", wraplength=950).pack(anchor="w", pady=3)
        self.config_editor = self.text_area(f, height=10)
        self.config_editor.insert("1.0", "{}")
        buttons = ttk.Frame(f)
        buttons.pack(fill="x", pady=5)
        ttk.Button(buttons, text="Driverconfiguratie toepassen", command=lambda: self.guarded(self.apply_config)).pack(side="left")
        ttk.Button(buttons, text="Instellingen / registergrenzen bekijken", command=self.show_schema).pack(side="left", padx=5)
        ttk.Label(f, text="chopper: spreadcycle / stealthchop · microsteps · full_steps_per_rev · irun / ihold · iholddelay\n"
                  "vref_v / rsense_ohm: invoer/aannames voor theoretische stroom; geen stroommeting.", wraplength=900).pack(anchor="w")

    def text_area(self, parent, height=10):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        text = tk.Text(frame, height=height, wrap="none", undo=True)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        return text

    def replace_text(self, widget, value):
        widget.delete("1.0", "end")
        widget.insert("1.0", json.dumps(value, indent=2, ensure_ascii=False))

    def set_driver_config(self, config):
        self.replace_text(self.config_editor, config)
        for key, var in self.basic_vars.items():
            if key in config:
                var.set(str(config[key]))

    def load_driver_profile(self):
        if self.driver_profile.get() in self.profiles:
            self.set_driver_config(self.profiles[self.driver_profile.get()])

    def get_driver_config(self):
        self.send("status", motor=self.motor.get(), callback=lambda result: self.set_driver_config(result["motors"][0]["config"]))

    def apply_basic(self):
        config = {key: (var.get() if key == "chopper" else float(var.get()) if key == "vref_v" else int(var.get()))
                  for key, var in self.basic_vars.items()}
        current = self.statuses.get(self.motor.get(), {}).get("config", {})
        if config["chopper"] == "stealthchop" and current.get("tpowerdown", 0) < 2:
            config["tpowerdown"] = 20
        self.send("configure", motor=self.motor.get(), config=config,
                  callback=lambda result: self.set_driver_config(result["config"]))

    def apply_config(self):
        config = json.loads(self.config_editor.get("1.0", "end"))
        if not isinstance(config, dict):
            raise ValueError("Configuratie moet een JSON-object zijn")
        self.send("configure", motor=self.motor.get(), config=config,
                  callback=lambda result: self.set_driver_config(result["config"]))

    def show_schema(self):
        window = tk.Toplevel(self.root)
        window.title("TMC2208 instellingen en grenzen")
        window.geometry("750x500")
        self.replace_text(self.text_area(window, 25), self.schema)

    def make_mechanics(self):
        f = self.tabs["Pintest"]
        self.mechanics_vars = {key: tk.StringVar(value="free" if key == "mode" else "") for key in
                               ("mode", "min_mm", "max_mm", "lead_mm_per_rev", "position_mm")}
        labels = {"mode": "Mechanische modus", "min_mm": "Expliciete minimumpositie (mm)", "max_mm": "Expliciete maximumpositie (mm)",
                  "lead_mm_per_rev": "Schroefspoed (mm per omwenteling)", "position_mm": "Handmatig vastgestelde startpositie (mm)"}
        for row, (key, var) in enumerate(self.mechanics_vars.items()):
            self.entry(f, row, labels[key], var, ["free", "pin"] if key == "mode" else None)
        buttons = ttk.Frame(f)
        buttons.grid(row=5, column=0, columnspan=2, sticky="w", pady=12)
        ttk.Button(buttons, text="Mechanische grenzen toepassen", command=lambda: self.guarded(self.apply_mechanics)).pack(side="left")
        ttk.Button(buttons, text="Startpositie opnieuw bevestigen", command=lambda: self.guarded(lambda: self.send(
            "reference", motor=self.motor.get(), position_mm=float(self.mechanics_vars["position_mm"].get())))).pack(side="left", padx=5)
        ttk.Label(f, text="50 mm pinlengte is geen 50 mm slag. Stel alleen fysiek gecontroleerde grenzen in.\n"
                  "Positie blijft berekend en kan door slip/stappenverlies afwijken. Er is geen automatische homing.\n"
                  "Na fout, noodstop of verbindingsverlies: positie handmatig controleren en referentie opnieuw bevestigen.",
                  wraplength=850).grid(row=6, column=0, columnspan=2, sticky="w")

    def apply_mechanics(self):
        settings = {"mode": self.mechanics_vars["mode"].get()}
        if settings["mode"] == "pin":
            settings.update({key: float(var.get()) for key, var in self.mechanics_vars.items() if key != "mode"})
        self.send("mechanics", motor=self.motor.get(), settings=settings)

    def make_automation(self):
        f = self.tabs["Automatische tests"]
        self.auto_vars = {key: tk.StringVar(value=value) for key, value in {
            "start": "10", "end": "50", "step": "10", "accelerations": "100", "choppers": "spreadcycle,stealthchop",
            "microsteps": "8", "currents": "5"}.items()}
        labels = {"start": "RPM start", "end": "RPM einde (indien op stapgrid)", "step": "RPM stap", "accelerations": "Acceleraties RPM/s (kommalijst)",
                  "choppers": "Choppermodi (kommalijst)", "microsteps": "Microstappen (kommalijst)", "currents": "IRUN-waarden (kommalijst)"}
        for row, (key, var) in enumerate(self.auto_vars.items()):
            self.entry(f, row, labels[key], var)
        ttk.Button(f, text="Start combinatietest", command=lambda: self.guarded(self.start_sweep)).grid(row=7, column=0, sticky="w", pady=8)
        self.auto_state = tk.StringVar(value="Geen automatische test actief")
        ttk.Label(f, textvariable=self.auto_state).grid(row=7, column=1, sticky="w")
        ttk.Label(f, text="Gebruikt bewegingsvorm, deceleratie, afstand/duur en cyclusvelden van Beweging.\n"
                  "Bij continuous wordt Duur gebruikt voor iedere eindige sweepstap. Alle combinaties worden vergeleken.\n"
                  "De eerste fout stopt de hele reeks. Hervat nooit automatisch na een fout of reconnect.",
                  wraplength=900).grid(row=8, column=0, columnspan=2, sticky="w")
        ttk.Button(f, text="Expliciete teststappen uit JSON…", command=lambda: self.guarded(self.load_steps)).grid(row=9, column=0, sticky="w", pady=8)

    def start_sweep(self):
        base = self.move_request()
        if base["mode"] == "continuous":
            base.update(mode="duration", duration_s=float(self.move_vars["duration_s"].get()))
        v = {key: var.get() for key, var in self.auto_vars.items()}
        def split(key, kind):
            return [kind(item.strip()) for item in v[key].split(",")]
        # Parse all list syntax now; firmware validates register limits transactionally per step.
        steps = comparison_steps(base, rpm_values(v["start"], v["end"], v["step"]),
                                 split("accelerations", float), split("choppers", str), split("microsteps", int), split("currents", int))
        self.send("_automation", motor=self.motor.get(), steps=steps)

    def file_dialog_allowed(self):
        active = any(s.get("state") in ("running", "warming", "holding") for s in self.worker.statuses.values())
        pending = any(not future.done() for future, _ in self.pending)
        if active or self.worker.records or self.worker.automation or pending or not self.worker.commands.empty():
            self.notice.set("Stop eerst alle motoren; een bestandsvenster mag STOP niet blokkeren tijdens een actieve test.")
            return False
        return True

    def load_steps(self):
        if not self.file_dialog_allowed():
            return
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            with open(path, encoding="utf-8") as stream:
                steps = json.load(stream)
            if not isinstance(steps, list) or not all(isinstance(step, dict) and "move" in step for step in steps):
                raise ValueError("Verwacht lijst met {config: {...}, move: {...}}")
            self.send("_automation", motor=self.motor.get(), steps=steps)

    def make_results(self):
        f = self.tabs["Resultaten"]
        self.result_tree = ttk.Treeview(f, columns=("motor", "source", "outcome", "rpm"), show="headings", height=5)
        for key, label in (("motor", "Motor"), ("source", "Herkomst"), ("outcome", "Uitkomst"), ("rpm", "Ingestelde RPM")):
            self.result_tree.heading(key, text=label)
            self.result_tree.column(key, width=150)
        self.result_tree.pack(fill="x")
        fields = ttk.Frame(f)
        fields.pack(fill="x", pady=5)
        self.measure_vars = {}
        names = [("displacement_mm", "Verplaatsing mm"), ("revolutions", "Omwentelingen"), ("rpm", "Echte RPM"), ("load_g", "Last g"),
                 ("vref_v", "Vref V"), ("vm_v", "VM V"), ("motor_temperature_c", "Motortemperatuur °C")]
        for index, (key, label) in enumerate(names):
            self.measure_vars[key] = tk.StringVar()
            ttk.Label(fields, text=label).grid(row=index // 3 * 2, column=index % 3, sticky="w")
            ttk.Entry(fields, textvariable=self.measure_vars[key]).grid(row=index // 3 * 2 + 1, column=index % 3, sticky="ew", padx=3)
        self.method = tk.StringVar()
        self.observation = tk.StringVar()
        self.measure_provenance = tk.StringVar(value="manual_measurement")
        self.entry(fields, 6, "Meetmethode / instrument", self.method)
        self.entry(fields, 7, "Provenance", self.measure_provenance, ["manual_measurement", "instrument_measurement"])
        self.entry(fields, 8, "Vrije waarneming (geen meting)", self.observation)
        buttons = ttk.Frame(f)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Metingen aan selectie toevoegen", command=lambda: self.guarded(self.add_measurements)).pack(side="left")
        ttk.Button(buttons, text="JSON export…", command=lambda: self.export("json")).pack(side="left", padx=4)
        ttk.Button(buttons, text="CSV export…", command=lambda: self.export("csv")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Kalibratie…", command=self.calibrate).pack(side="left", padx=4)
        ttk.Label(f, text="Lege velden blijven onbekend. Iedere test bevat instellingen, berekende beweging, diagnose en UART-tellers.\n"
                  "Metingen horen bij de geselecteerde test. Exporteer vóór het sluiten; testresultaten blijven tot dan in geheugen.", wraplength=900).pack(anchor="w")

    def selected_record(self):
        selected = self.result_tree.selection()
        if not selected:
            raise ValueError("Selecteer eerst een testresultaat")
        return next(record for record in self.worker.results.records if record["test_id"] == selected[0])

    def add_measurements(self):
        with self.worker.lock:
            self.worker.results.measure(self.selected_record(), {key: var.get() for key, var in self.measure_vars.items()},
                                        self.method.get(), self.observation.get(), self.measure_provenance.get())
        self.notice.set("Ingevoerde metingen en herkomst opgeslagen bij de geselecteerde test.")

    def export(self, kind):
        if not self.file_dialog_allowed():
            return
        path = filedialog.asksaveasfilename(defaultextension="." + kind, filetypes=[(kind.upper(), "*." + kind)])
        if path:
            def write():
                with self.worker.lock:
                    getattr(self.worker.results, "export_" + kind)(path)
                self.notice.set("Resultaten geëxporteerd naar " + path)
            self.guarded(write)

    def calibrate(self):
        window = tk.Toplevel(self.root)
        selected_motor = self.motor.get()
        window.title("Kalibratie met handmatige meting · " + selected_motor)
        window.geometry("620x370")
        config = self.statuses.get(selected_motor, {}).get("config", {})
        variables = {key: tk.StringVar(value=value) for key, value in {
            "previous": str(config.get("calibration_factor", 1)), "calculated_rev": "", "measured_rev": "", "measured_mm": "", "lead": ""}.items()}
        labels = {"previous": "Huidige kalibratiefactor", "calculated_rev": "Berekende omwentelingen van deze proef", "measured_rev": "Werkelijk gemeten omwentelingen (of leeg)",
                  "measured_mm": "Gemeten verplaatsing mm (of leeg)", "lead": "Spoed mm/omwenteling (bij verplaatsing)"}
        for row, (key, var) in enumerate(variables.items()):
            self.entry(window, row, labels[key], var)
        result = tk.StringVar(value="Voer precies één echte meting in; gebruik een eenrichtingsproef.")
        ttk.Label(window, textvariable=result, wraplength=580).grid(row=5, column=0, columnspan=2, pady=8)
        def compute(apply=False):
            values = {key: var.get() for key, var in variables.items()}
            factor = calibration_factor(values["previous"], values["calculated_rev"], values["measured_rev"] or None,
                                        values["measured_mm"] or None, values["lead"] or None)
            result.set("Nieuwe factor: %.9g · corrigeert schaal, geen slip/stappenverlies." % factor)
            if apply:
                self.send("configure", motor=selected_motor, config={"calibration_factor": factor})
        ttk.Button(window, text="Bereken", command=lambda: self.guarded(compute)).grid(row=6, column=0)
        ttk.Button(window, text="Bereken en pas toe (stilstaand)", command=lambda: self.guarded(lambda: compute(True))).grid(row=6, column=1)

    def make_diagnostics(self):
        f = self.tabs["Diagnostiek"]
        buttons = ttk.Frame(f)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Driverdiagnose verversen", command=lambda: self.send("diagnose", motor=self.motor.get())).pack(side="left")
        ttk.Button(buttons, text="Fout wissen na controle", command=lambda: self.send("clear_fault", motor=self.motor.get())).pack(side="left", padx=5)
        ttk.Label(f, text="Temperatuurwaarschuwingen komen uit de driver; dit is geen motor-/positiemeting en geen stalldetectie.", wraplength=950).pack(anchor="w", pady=5)
        self.diagnostics = self.text_area(f, 24)

    def profile(self):
        return {"motor": self.motor.get(), "move": {key: value.get() for key, value in self.move_vars.items()},
                "mechanics": {key: value.get() for key, value in self.mechanics_vars.items()},
                "automation": {key: value.get() for key, value in self.auto_vars.items()},
                "driver": json.loads(self.config_editor.get("1.0", "end")),
                "driver_basic": {key: var.get() for key, var in self.basic_vars.items()}}

    def save(self):
        if not self.file_dialog_allowed():
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Profiel JSON", "*.json")])
        if path:
            self.guarded(lambda: save_profile(path, self.profile()))

    def load(self):
        if not self.file_dialog_allowed():
            return
        path = filedialog.askopenfilename(filetypes=[("Profiel JSON", "*.json")])
        if path:
            def apply():
                profile = load_profile(path)
                for key, target in (("move", self.move_vars), ("mechanics", self.mechanics_vars), ("automation", self.auto_vars)):
                    for name, value in profile.get(key, {}).items():
                        if name in target:
                            target[name].set(value)
                if "driver" in profile:
                    self.set_driver_config(profile["driver"])
                for key, value in profile.get("driver_basic", {}).items():
                    if key in self.basic_vars:
                        self.basic_vars[key].set(value)
                if profile.get("motor") in self.motor_box["values"]:
                    self.motor.set(profile["motor"])
                self.notice.set("Profiel geladen in invoervelden. Pas driver en mechanica expliciet toe vóór Start.")
            self.guarded(apply)

    def select_motor(self):
        self.refresh_selected()
        self.get_driver_config()
        mechanics = self.statuses.get(self.motor.get(), {}).get("mechanics", {})
        for key, var in self.mechanics_vars.items():
            var.set("" if key == "position_mm" else str(mechanics.get(key, "free" if key == "mode" else "")))
        self.notice.set("Motor %s geselecteerd. Een pinreferentie blijft een handmatige controle." % self.motor.get())

    def refresh_selected(self):
        status = self.statuses.get(self.motor.get(), {})
        motion = status.get("motion", {})
        self.summary.set("%s · %s · RPM ingesteld %s / berekend %s · positie %.5g omw · afstand %.5g omw · %.2f s" % (
            self.motor.get(), status.get("state", "onbekend"), motion.get("rpm_requested", "?"),
            motion.get("rpm_calculated", "?"), motion.get("position_rev_calculated", 0),
            motion.get("distance_rev_calculated", 0), motion.get("elapsed_s", 0)))
        self.replace_text(self.diagnostics, status)

    def update_results(self):
        with self.worker.lock:
            for record in self.worker.results.records:
                key = record["test_id"]
                values = (record["motor"], record["source"], record["outcome"], record["requested"].get("rpm", "—"))
                if key in self.last_record_ids:
                    self.result_tree.item(key, values=values)
                else:
                    self.result_tree.insert("", "end", iid=key, values=values)
                    self.last_record_ids.add(key)

    def pump(self):
        for future, callback in self.pending[:]:
            if future.done():
                self.pending.remove((future, callback))
                try:
                    result = future.result()
                    if callback:
                        callback(result)
                except Exception as exc:
                    self.notice.set(str(exc))
        while True:
            try:
                event = self.worker.events.get_nowait()
            except queue.Empty:
                break
            kind = event["event"]
            if kind == "ports":
                choices = [p["device"] for p in event["ports"]] + ["SIMULATIE"]
                self.port_box.configure(values=choices)
                if not self.port.get() and event["ports"]:
                    candidates = [p for p in event["ports"] if "pico" in p["description"].lower() or "micropython" in p["description"].lower()]
                    self.port.set((candidates or event["ports"])[0]["device"])
            elif kind == "connection":
                if event["connected"]:
                    self.connection.set(("SIMULATIE · " if event["simulated"] else "Verbonden · ") + event["port"] + " · " + str(event["hello"].get("firmware", "")))
                    motors = event["hello"].get("motors", [])
                    self.motor_box.configure(values=motors)
                    if motors and self.motor.get() not in motors:
                        self.motor.set(motors[0])
                    self.profiles = event["hello"].get("profiles", {})
                    self.schema = event["hello"].get("config_schema", {})
                    self.profile_box.configure(values=list(self.profiles))
                    if self.profiles:
                        self.driver_profile.set(next(iter(self.profiles)))
                    self.get_driver_config()
                    self.notice.set("Verbonden; er wordt geen beweging automatisch hervat.")
                else:
                    self.connection.set("Niet verbonden · " + event.get("error", ""))
            elif kind == "status":
                self.statuses = event["statuses"]
                self.refresh_selected()
                self.update_results()
            elif kind == "automation":
                self.auto_state.set("%s · stap %s · %s" % (event["state"], event.get("index", "—"), event.get("error", "")))
                self.update_results()
            elif kind in ("error", "stopped"):
                self.notice.set(event.get("message", ""))
        if self.closing:
            if self.worker.is_alive():
                self.root.after(50, self.pump)
            else:
                self.root.destroy()
        else:
            self.root.after(50, self.pump)

    def close(self):
        self.closing = True
        self.worker.shutdown()
        self.notice.set("STOP en verbinding afsluiten…")


def main():
    parser = argparse.ArgumentParser(description="E-302 Tkinter testomgeving")
    parser.add_argument("--simulate", action="store_true", help="Gebruik echte firmware met gesimuleerde driver")
    args = parser.parse_args()
    root = tk.Tk()
    Application(root, simulate=args.simulate)
    root.mainloop()


if __name__ == "__main__":
    main()
