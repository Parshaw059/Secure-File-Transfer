
SECURE FILE TRANSFER — Monitoring & Integrity System

INSTALL:
pip install -r requirements.txt

RUN (single process — starts monitor + dashboard together):
python app.py

OPEN:
http://127.0.0.1:8000

TEST:
Create, modify, or delete files inside the sensitive_data folder.
The dashboard updates automatically every 5 seconds.

NOTE:
app.py now starts the file-system monitor (main.py) on a background
thread automatically, so only one process is needed to run the full
system locally or on a cloud host such as Render.
