from flask import Flask, render_template, redirect, url_for
import os
import threading
import time
import datetime

app = Flask(__name__)
LOG_FILE = "audit_log.txt"
SENSITIVE_DIR = "sensitive_data"

def start_monitor():
    import main
    
@app.route("/")
def index():
    logs = []
    alerts = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.readlines()[-100:]
            alerts = sum(1 for line in logs if "ALERT" in line)
    return render_template("index.html", logs=reversed(logs), total_events=len(logs), alerts=alerts)

@app.route("/test")
def run_test():
    os.makedirs(SENSITIVE_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    test_file = os.path.join(SENSITIVE_DIR, f"sensitivity_test_{timestamp}.txt")

    def create_and_delete():
        with open(test_file, "w") as f:
            f.write("SENSITIVITY TEST FILE\n")
            f.write(f"Created at: {datetime.datetime.now()}\n")
            f.write("This file verifies SENSITIVE=True detection.\n")
        time.sleep(2)
        with open(test_file, "a") as f:
            f.write("Modified to verify hash change detection.\n")
        time.sleep(2)
        if os.path.exists(test_file):
            os.remove(test_file)

    threading.Thread(target=create_and_delete, daemon=True).start()
    return redirect(url_for("index"))

@app.route("/clear")
def clear_log():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
    return redirect(url_for("index"))

monitor_thread = threading.Thread(target=start_monitor, daemon=True)
monitor_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
