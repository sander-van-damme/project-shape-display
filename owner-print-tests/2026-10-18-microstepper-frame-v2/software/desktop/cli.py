"""Minimal console controller using the same worker/heartbeat/logging as the GUI."""
import argparse
import json
import sys
import time
from .transport import ports
from .worker import SessionWorker


def wait_idle(worker):
    # No arbitrary run time ceiling: firmware state determines completion.
    while worker.records or worker.automation:
        if worker.link is None:
            raise OSError("Verbinding verloren; test afgebroken")
        time.sleep(0.05)
    if worker.automation_error:
        raise RuntimeError(worker.automation_error)
    if worker.results.records and worker.results.records[-1]["outcome"] not in ("completed", "stopped"):
        raise RuntimeError(worker.results.records[-1].get("error", "Test mislukt"))


def submit_line(worker, line, motor):
    line = line.strip()
    if line == "!":
        worker.stop_now()
        return {"stop": "requested"}
    if line in ("hello", "status", "stop", "diagnose", "clear_fault"):
        request = {"cmd": line}
    else:
        request = json.loads(line)
    if not isinstance(request, dict) or "cmd" not in request:
        raise ValueError("Geef een JSON-object met cmd op")
    request = request.copy()
    command = request.pop("cmd")
    request.pop("id", None)
    if command not in ("hello", "status", "heartbeat"):
        request.setdefault("motor", motor)
    return worker.submit(command, **request).result(timeout=15)


def main(argv=None):
    parser = argparse.ArgumentParser(description="E-302 lokale CLI (Ctrl+C of ! = stop)")
    parser.add_argument("--port", help="COM7 of /dev/ttyACM0")
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--motor", default="m1")
    parser.add_argument("--export", help="Resultaatbestand .csv of .json")
    sub = parser.add_subparsers(dest="action")
    sub.add_parser("ports", help="Zoek seriële poorten")
    sub.add_parser("shell", help="Interactieve JSON-opdrachten met achtergrondheartbeat")
    sub.add_parser("demo", help="Korte gesimuleerde of fysieke eindige proef")
    request = sub.add_parser("request", help="Eén JSON-opdracht; eindige beweging wordt afgewacht")
    request.add_argument("json")
    run = sub.add_parser("run", help="Eindige teststappen uit JSON; stopt op eerste fout")
    run.add_argument("file")
    args = parser.parse_args(argv)
    if args.action == "ports":
        print(json.dumps(ports(), indent=2))
        return 0
    if not args.simulate and not args.port:
        parser.error("Gebruik --port COM7 of --simulate")
    worker = SessionWorker()
    worker.start()
    exit_code = 0
    try:
        hello = worker.connect("SIMULATIE" if args.simulate else args.port, reconnect=False).result(timeout=15)
        print(json.dumps({"firmware": hello.get("firmware"), "motors": hello.get("motors"), "simulated": args.simulate}, ensure_ascii=False))
        if args.action == "demo":
            worker.submit("move", motor=args.motor, mode="revolutions", rpm=30, accel=100,
                          decel=100, revolutions=0.25).result(timeout=15)
            wait_idle(worker)
            print(json.dumps({key: worker.results.records[-1][key] for key in ("test_id", "source", "outcome", "calculated")}, indent=2))
        elif args.action == "run":
            with open(args.file, encoding="utf-8") as stream:
                steps = json.load(stream)
            if not isinstance(steps, list):
                raise ValueError("Testbestand moet een lijst van config/move-objecten bevatten")
            worker.submit("_automation", motor=args.motor, steps=steps).result(timeout=15)
            wait_idle(worker)
            print(json.dumps({"completed_tests": len(worker.results.records)}))
        elif args.action == "request":
            parsed = json.loads(args.json)
            if parsed.get("cmd") == "move" and parsed.get("mode") == "continuous":
                raise ValueError("Gebruik shell voor continu draaien; de CLI stopt bij afsluiten")
            print(json.dumps(submit_line(worker, args.json, args.motor), indent=2))
            wait_idle(worker)
        else:
            print('JSON per regel; status / diagnose / stop / clear_fault / ! / quit. Heartbeat blijft actief.\n'
                  'Voorbeeld: {"cmd":"move","mode":"continuous","rpm":30,"accel":100,"decel":100}')
            while True:
                try:
                    line = input("e302> ")
                except EOFError:
                    break
                if line.strip() in ("quit", "exit"):
                    break
                if not line.strip():
                    continue
                try:
                    print(json.dumps(submit_line(worker, line, args.motor), indent=2))
                except Exception as exc:
                    print("Fout: " + str(exc), file=sys.stderr)
    except KeyboardInterrupt:
        print("STOP aangevraagd", file=sys.stderr)
        exit_code = 130
    except Exception as exc:
        print("Fout: " + str(exc), file=sys.stderr)
        exit_code = 1
    finally:
        worker.shutdown()
        worker.join(timeout=5)
        if args.export:
            with worker.lock:
                if args.export.lower().endswith(".csv"):
                    worker.results.export_csv(args.export)
                else:
                    worker.results.export_json(args.export)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
