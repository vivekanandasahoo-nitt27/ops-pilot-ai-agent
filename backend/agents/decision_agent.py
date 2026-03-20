from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def decision_agent(state: dict):

    text = state.get("incident_text", "").lower()

    # 🔴 RULE 1: PAYMENT → ALWAYS ALERT
    if any(word in text for word in ["payment", "amount", "rs", "rupees", "money", "invoice"]):
        print("⚠️ Rule-based override: ALERT")
        state["decision"] = "ALERT"
        return state

    # 🟡 RULE 2: MEETING → ALWAYS HUMAN_REQUIRED
    if any(word in text for word in ["meeting", "call", "schedule", "appointment"]):
        print("⚠️ Rule-based override: HUMAN_REQUIRED")
        state["decision"] = "HUMAN_REQUIRED"
        return state

    # 🧠 FALLBACK → LLM
    prompt = f"""
    You are an enterprise AI decision system.

    Analyze this message:

    {text}

    RULES:

    🔴 ALERT:
    - Payment, money, financial transactions
    - Security threats

    🟡 HUMAN_REQUIRED:
    - Meetings, calls, scheduling
    - Requests needing human confirmation

    🟢 AUTO_REPLY:
    - Greetings, casual chat

    STRICT:
    - Meetings are NOT alerts
    - Only financial/security = ALERT

    Return ONLY:
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