from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def decision_agent(state: dict):

    text = state.get("incident_text", "")

    prompt = f"""
    You are an enterprise AI risk detection system.

    Analyze this email:

    {state.get("incident_text")}

    STRICT RULES:

    🔴 ALERT (High Risk):
    - Any payment, money, transaction, amount
    - Pending payment, invoices, financial requests
    - Fraud, security, unauthorized activity

    🟡 HUMAN_REQUIRED:
    - Meetings, scheduling, approvals
    - Requests needing human confirmation

    🟢 AUTO_REPLY:
    - Greetings, casual messages

    IMPORTANT:
    - If ANY money/amount/payment is mentioned → ALWAYS ALERT
    - Even small amount → ALERT

    Return ONLY one word:
    AUTO_REPLY
    HUMAN_REQUIRED
    ALERT
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    decision = response.choices[0].message.content.strip().upper()

    # 🔥 CLEAN OUTPUT
    if "AUTO" in decision:
        decision = "AUTO_REPLY"
    elif "HUMAN" in decision:
        decision = "HUMAN_REQUIRED"
    elif "ALERT" in decision:
        decision = "ALERT"
    else:
        decision = "HUMAN_REQUIRED"

    print("🧠 Decision Agent Output:", decision)

    state["decision"] = decision

    return state