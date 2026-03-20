from agents.classifier_agent import classifier_agent

state = {
    "incident_text": "Multiple failed login attempts detected"
}

result = classifier_agent(state)

print(result)