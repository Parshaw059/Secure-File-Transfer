
from flask import Flask, render_template
import os
import threading

app = Flask(__name__)
LOG_FILE = "audit_log.txt"

def start_monitor():
    """Runs the file-system monitor (main.py logic) on a background thread,
    so a single deployed process handles both monitoring and the dashboard."""
    import main  # noqa: starts the watchdog observer as an import side-effect

@app.route("/")
def index():
    logs = []
    alerts = 0

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()[-100:]
            alerts = sum(1 for line in logs if "ALERT" in line)

    return render_template(
        "index.html",
        logs=reversed(logs),
        total_events=len(logs),
        alerts=alerts
    )

# Start the monitor once, in the background, when the app boots.
monitor_thread = threading.Thread(target=start_monitor, daemon=True)
monitor_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
