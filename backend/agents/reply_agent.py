from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def reply_agent(state: dict):

    incident_text = state.get("incident_text", "")
    human_input = state.get("human_input", "")

    # 🔥 STEP 1: Extract structured info
    extraction_prompt = f"""
Extract important details from this email.

Email:
{incident_text}

Additional Human Instruction:
{human_input}

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- If not found, keep empty string

Format:
{{
  "type": "meeting / casual / other",
  "time": "",
  "person": "",
  "summary": ""
}}
"""

    extraction = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": extraction_prompt}]
    )

    extracted_text = extraction.choices[0].message.content.strip()

    # 🔥 Safe JSON parsing
    try:
        extracted_data = json.loads(extracted_text)
    except:
        print("⚠️ JSON parsing failed, using fallback")
        extracted_data = {
            "type": "unknown",
            "time": "",
            "person": "",
            "summary": ""
        }

    print("🧠 Extracted Data:", extracted_data)

    # 🔥 STEP 2: Generate smart reply
    reply_prompt = f"""
You are a smart email assistant.

Email:
{incident_text}

Additional Human Instruction:
{human_input}


Extracted Data:
Type: {extracted_data.get("type")}
Time: {extracted_data.get("time")}
Person: {extracted_data.get("person")}

Instructions:
- If meeting → confirm time and person clearly
- If casual → friendly short reply
- Keep it natural and human tone  and short (1–2 lines)
- please include the human input in the reply all the details and information given be the human
- DO NOT give generic replies like "Thanks, let's proceed"

Examples:
- "Got it, see you tomorrow at 11 AM with Subhas 👍"
- "Sounds good, I’ll be there at the scheduled time."
- if it was a casual message so reply in a human manner and in friendly manner 
- case of ALERT like payment unauthorised work please include all the improtant information like name of requester amount purpose

Now generate the reply:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": reply_prompt}]
    )

    reply = response.choices[0].message.content.strip()

    print("📧 Generated Reply:", reply)

    state["auto_reply"] = reply

    return state