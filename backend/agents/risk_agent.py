from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def risk_agent(state: dict):

    incident_text = state["incident_text"]
    incident_type = state["incident_type"]

    prompt = f"""
You are a cybersecurity incident analysis AI.

Your job is to assign a severity level.

Incident Type: {incident_type}
Incident Description: {incident_text}

Rules:
- Unauthorized access attempts or repeated login failures → HIGH
- Service disruption or degraded performance → MEDIUM
- Informational or minor warnings → LOW

Return ONLY one word:
HIGH
MEDIUM
LOW
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    severity = response.choices[0].message.content.strip().upper()

    # extra safety cleanup
    if "HIGH" in severity:
        severity = "HIGH"
    elif "MEDIUM" in severity:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    state["severity"] = severity

    return state