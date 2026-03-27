from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classifier_agent(state: dict):

    incident_text = state["incident_text"]

    prompt = f"""
Classify the following email into one category.

Categories:
- Security → unauthorized access, hacking, alerts
- System Failure → server down, crash, errors
- Payment Risk → money, transactions, fraud
- Compliance Issue → policy violation, legal issue
- Meeting → scheduling, discussion, appointments
- Casual → greetings, normal conversation
- Other → anything else

Rules:
- Return ONLY the category name
- Do NOT explain
- Choose the closest category

Email:
{incident_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    category = response.choices[0].message.content.strip().split("\n")[0]
    category = category.replace(".", "").strip()

    state["incident_type"] = category

    return state