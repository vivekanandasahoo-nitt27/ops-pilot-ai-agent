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
You are a professional email assistant and u need to reply like a human consider yourself as human and reply with all the information  .

Your job is to generate a short.

Email:
{incident_text}

Additional Human Instruction:
{human_input}

Extracted Data:
Type: {extracted_data.get("type")}
Time: {extracted_data.get("time")}
Person: {extracted_data.get("person")}

STRICT RULES:
- Output ONLY the final email reply text
- DO NOT explain anything
- DO NOT add assumptions
- DO NOT correct names unless explicitly given
- DO NOT add notes like (I assumed...)
- DO NOT hallucinate any information
- Keep reply short (1–2 lines max)
- Keep tone natural and human
- If human_input exists → MUST include it clearly
- If information is missing → do NOT guess

STYLE:
- Meeting → confirm time clearly given in the email
- Casual → friendly and simple and natural
- Alert → clear and serious

GOOD EXAMPLES:
- "Got it, I’ll be there tomorrow at 11:30 AM."
- "I’ll take care of the documents before the meeting. and for meeting provide all the document"
- "Noted, I’ll review everything and update you shortly."

Now generate ONLY the reply:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": reply_prompt}]
    )

    reply = response.choices[0].message.content.strip()

    print("📧 Generated Reply:", reply)

    state["auto_reply"] = reply

    return state