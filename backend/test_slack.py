from integrations.slack import send_slack_alert

state = {
    "incident_text": "Test security alert",
    "incident_type": "Security",
    "severity": "HIGH",
    "source_system": "demo-system"
}

send_slack_alert(state)

print("Slack message sent")