import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(state):

    message = {
        "text": f"""
🚨 Incident Alert

Incident: {state['incident_text']}
Type: {state['incident_type']}
Decision: {state.get('decision', 'N/A')}
System: {state['source_system']}
"""
    }

    requests.post(SLACK_WEBHOOK, json=message)