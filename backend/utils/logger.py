import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs.json")

def log_event(state):

    log_entry = {
        "timestamp": str(datetime.now()),
        "message": state.get("incident_text"),
        "decision": state.get("decision"),
        "action": state.get("action_taken"),
        "system": state.get("source_system")
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)