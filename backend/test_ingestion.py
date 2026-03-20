from agents.ingestion_agent import ingestion_agent

alert = {
    "alert": "Multiple failed login attempts detected",
    "system": "authentication-server"
}

result = ingestion_agent(alert)

print(result)