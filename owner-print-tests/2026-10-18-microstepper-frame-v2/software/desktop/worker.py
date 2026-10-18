"""One serial owner; Tk stays responsive, STOP preempts reads and queued commands."""
import queue
import threading
import time
from concurrent.futures import Future
from .model import Results
from .transport import CommandError, SerialLink, SimulatedLink, StopRequested, ports


ACTIVE = ("running", "warming")
FINISHED = ("idle", "holding")


class SessionWorker(threading.Thread):
    def __init__(self, link_factory=None):
        super().__init__(name="e302-serial", daemon=True)
        self.commands = queue.Queue()
        self.events = queue.Queue()
        self.stop_event = threading.Event()
        self.quit_event = threading.Event()
        self.link = None
        self.link_factory = link_factory
        self.desired_port = None
        self.reconnect = True
        self.retry_at = 0
        self.next_heartbeat = self.next_poll = self.next_scan = 0
        self.statuses = {}
        self.hello = {}
        self.results = Results()
        self.records = {}
        self.automation = None
        self.automation_error = None
        self.lock = threading.RLock()

    def emit(self, event, **data):
        self.events.put(dict(data, event=event))

    def submit(self, command, **parameters):
        future = Future()
        self.commands.put((command, parameters, future))
        return future

    def connect(self, port, reconnect=True):
        return self.submit("_connect", port=port, reconnect=reconnect)

    def stop_now(self):
        self.stop_event.set()

    def shutdown(self):
        self.stop_event.set()
        self.quit_event.set()

    def _request(self, cmd, **parameters):
        if self.link is None:
            raise CommandError("Niet verbonden")
        if self.stop_event.is_set():
            self.link.emergency_stop()
            raise StopRequested("STOP vóór commando")
        return self.link.request(dict(parameters, cmd=cmd))

    def _finish_records(self, outcome, error=None):
        with self.lock:
            for record in self.records.values():
                self.results.finish(record, outcome, error)
            self.records.clear()
        if self.automation is not None:
            self.automation = None
            self.emit("automation", state=outcome, error=str(error or ""))

    def _cancel_queue(self):
        while True:
            try:
                _, _, future = self.commands.get_nowait()
                if not future.done():
                    future.set_exception(StopRequested("Commando geannuleerd door STOP"))
            except queue.Empty:
                return

    def _handle_stop(self):
        self._cancel_queue()
        self._finish_records("stopped", "STOP door gebruiker")
        self.stop_event.clear()
        if self.link is not None:
            self.link.emergency_stop()
        self.emit("stopped", message="STOP verzonden; controleer status en fysieke beweging")
        self.next_poll = 0

    def _disconnect(self, error=None):
        self._cancel_queue()
        old_link, self.link = self.link, None
        if old_link:
            try:
                old_link.emergency_stop()
            except Exception:
                pass
            try:
                old_link.close()
            except Exception:
                pass
        self._finish_records("disconnected", error or "Verbinding beëindigd")
        self.statuses = {}
        self.emit("connection", connected=False, error=str(error or ""))
        self.retry_at = time.monotonic() + 2

    def _open(self):
        if self.link_factory:
            link = self.link_factory(self.desired_port, self.stop_event)
        elif self.desired_port == "SIMULATIE":
            link = SimulatedLink()
        else:
            link = SerialLink(self.desired_port, self.stop_event)
        self.link = link
        # Never restore a previous command after reattachment.
        link.emergency_stop()
        self.hello = self._request("hello")
        if self.hello.get("protocol") != 1:
            raise OSError("Niet-ondersteunde protocolversie")
        self.next_heartbeat = self.next_poll = 0
        self.emit("connection", connected=True, port=self.desired_port, hello=self.hello,
                  simulated=link.simulated)

    def _begin_move(self, parameters):
        motor = parameters["motor"]
        status = self.statuses.get(motor)
        if status is None:
            reply = self._request("status", motor=motor)
            status = reply["motors"][0]
        result = self._request("move", **parameters)
        with self.lock:
            self.records[motor] = self.results.begin(motor, parameters, status.get("config", {}), self.link.simulated)
        self.next_poll = 0
        return result

    def _next_step(self):
        auto = self.automation
        if auto is None:
            return
        try:
            step = next(auto["steps"])
        except StopIteration:
            self.automation = None
            self.emit("automation", state="completed")
            return
        except Exception as exc:
            self._automation_error(exc)
            return
        try:
            if self.stop_event.is_set():
                raise StopRequested("STOP")
            if not isinstance(step, dict) or not isinstance(step.get("move"), dict) or not isinstance(step.get("config", {}), dict):
                raise CommandError("Een teststap vereist config/move-objecten")
            motor = auto["motor"]
            if step.get("config"):
                result = self._request("configure", motor=motor, config=step["config"])
                if isinstance(result, dict):
                    self.statuses[motor] = result
            move = dict(step["move"], motor=motor)
            if move.get("mode") == "continuous":
                raise CommandError("Sweep vereist eindige beweging")
            self._begin_move(move)
            auto["index"] += 1
            auto["awaiting"] = True
            self.emit("automation", state="running", index=auto["index"], step=step)
        except StopRequested:
            raise
        except OSError:
            raise
        except Exception as exc:
            # Failed configuration/start is itself a test outcome with provenance.
            with self.lock:
                record = self.results.begin(auto["motor"], step if isinstance(step, dict) else {"invalid_step": step}, self.statuses.get(auto["motor"], {}).get("config", {}), self.link.simulated)
                self.results.finish(record, "failed", exc)
            self._automation_error(exc)

    def _automation_error(self, error):
        self.automation = None
        self.automation_error = str(error)
        if self.link:
            self.link.emergency_stop()
        self.emit("automation", state="failed", error=str(error))

    def _poll(self):
        reply = self._request("status")
        self.statuses = {s["motor"]: s for s in reply.get("motors", [])}
        advance = False
        for motor, status in self.statuses.items():
            record = self.records.get(motor)
            if record:
                with self.lock:
                    self.results.sample(record, status)
                    if status.get("fault") or status.get("state") == "fault":
                        self.results.finish(record, "failed", status.get("fault", "Driverfout"))
                        del self.records[motor]
                        if self.automation is not None:
                            self._automation_error(status.get("fault", "Driverfout"))
                    elif status.get("state") in FINISHED:
                        motion = status.get("motion", {})
                        completed = motion.get("completed") is True and motion.get("completion_reason") == "completed"
                        reason = motion.get("completion_reason", "incomplete")
                        outcome = "completed" if completed else ("stopped" if reason in ("stopped", "emergency_stop") else "incomplete")
                        self.results.finish(record, outcome, None if completed else reason)
                        del self.records[motor]
                        if self.automation and self.automation["motor"] == motor:
                            if completed:
                                advance = True
                            else:
                                self._automation_error("Test onvolledig: " + str(reason))
        self.emit("status", statuses=self.statuses, usb=dict(self.link.stats))
        if advance:
            self._next_step()

    def _dispatch(self, command, parameters):
        if command == "_connect":
            self.desired_port = parameters["port"]
            self.reconnect = parameters.get("reconnect", True)
            self._disconnect()
            self._open()
            return self.hello
        if command == "_disconnect":
            self.desired_port = None
            self._disconnect()
            return {}
        if command == "_automation":
            if self.link is None:
                raise CommandError("Niet verbonden")
            motor = parameters["motor"]
            if self.automation or motor in self.records:
                raise CommandError("Er loopt al een test; stop deze eerst")
            self.automation_error = None
            self.automation = {"motor": motor, "steps": iter(parameters["steps"]), "index": 0, "awaiting": False}
            self._next_step()
            return {"started": True}
        if command == "move":
            return self._begin_move(parameters)
        if command == "stop" and self.automation:
            self.automation = None
            self.emit("automation", state="stopped")
        result = self._request(command, **parameters)
        self.next_poll = 0
        return result

    def run(self):
        try:
            while not self.quit_event.is_set():
                try:
                    if self.stop_event.is_set():
                        self._handle_stop()
                    now = time.monotonic()
                    if now >= self.next_scan:
                        self.emit("ports", ports=ports())
                        self.next_scan = now + 2
                    if self.link:
                        self.link.tick()
                        if now >= self.next_heartbeat:
                            self._request("heartbeat")
                            self.next_heartbeat = time.monotonic() + 0.5
                        if now >= self.next_poll:
                            self._poll()
                            self.next_poll = time.monotonic() + 0.2
                    elif self.desired_port and self.reconnect and now >= self.retry_at:
                        self._open()
                    try:
                        command, parameters, future = self.commands.get(timeout=0.01)
                    except queue.Empty:
                        continue
                    try:
                        result = self._dispatch(command, parameters)
                    except StopRequested as exc:
                        future.set_exception(exc)
                        self._handle_stop()
                    except OSError as exc:
                        future.set_exception(exc)
                        self._disconnect(exc)
                    except Exception as exc:
                        future.set_exception(exc)
                        self.emit("error", message=str(exc))
                    else:
                        future.set_result(result)
                except StopRequested:
                    self._handle_stop()
                except Exception as exc:
                    self._disconnect(exc)
        finally:
            self.desired_port = None
            self._cancel_queue()
            self._disconnect("Applicatie gesloten")
