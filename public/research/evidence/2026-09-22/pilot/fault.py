"""Fault controller. The worker ANNOUNCES the fault point and then waits to be killed
by the parent; the process does not choose its own death. No cleanup path runs."""
import os, time

POINTS = ["AFTER_MODEL_BEFORE_CHECKPOINT", "AFTER_CHECKPOINT_BEFORE_WAIT", "AT_WAIT",
          "AFTER_EFFECT_COMMIT_BEFORE_ACK", "AFTER_ACK_BEFORE_NEXT_STEP"]

def announce_and_wait(marker_path, point, log=None):
    if os.environ.get("PILOT_NO_FAULT"):
        if log: log.emit(type="faultpoint.skipped", fault_point=point)
        return
    if log: log.emit(type="faultpoint.reached", fault_point=point)
    with open(marker_path, "w") as fh:
        fh.write(point); fh.flush(); os.fsync(fh.fileno())
    while True:            # parent sends SIGKILL here
        time.sleep(0.02)
