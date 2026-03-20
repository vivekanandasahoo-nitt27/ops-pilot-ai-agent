from agents.risk_agent import risk_agent

state = {
    "incident_text": "Multiple failed login attempts detected",
    "incident_type": "Security"
}

result = risk_agent(state)

print(result)