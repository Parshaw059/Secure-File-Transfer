
import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "audit_log.txt"
SENSITIVE_DIRS = ["sensitive_data"]

def sha256_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                h.update(chunk)
        return h.hexdigest()
    except:
        return "UNAVAILABLE"

def log_event(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

class MonitorHandler(FileSystemEventHandler):

    def process(self, event, action):

        if event.is_directory:
            return

        if os.path.basename(event.src_path) == LOG_FILE:
            return

        path = event.src_path

        sensitive = any(s in path for s in SENSITIVE_DIRS)

        hash_value = sha256_file(path) if os.path.isfile(path) else "N/A"

        message = (
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"ACTION={action} PATH={path} "
            f"SENSITIVE={sensitive} HASH={hash_value}"
        )

        log_event(message)

        if sensitive:
            log_event(f"ALERT: Sensitive file activity detected -> {path}")

    def on_created(self, event):
        self.process(event, "CREATED")

    def on_modified(self, event):
        self.process(event, "MODIFIED")

    def on_deleted(self, event):
        self.process(event, "DELETED")

    def on_moved(self, event):
        self.process(event, "MOVED")

observer = Observer()
observer.schedule(MonitorHandler(), ".", recursive=True)
observer.start()

print("Secure File Transfer Monitoring Started...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
