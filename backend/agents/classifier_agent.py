from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classifier_agent(state: dict):

    incident_text = state["incident_text"]

    prompt = f"""
    Classify the following enterprise incident into one category:

    Categories:
    Security
    System Failure
    Payment Risk
    Compliance Issue
    Other

    Incident:
    {incident_text}

    Return only the category name.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    category = response.choices[0].message.content.strip().split("\n")[0]

    state["incident_type"] = category

    return state