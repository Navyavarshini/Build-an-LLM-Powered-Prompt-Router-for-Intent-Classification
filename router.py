import os
from groq import Groq
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data.get("intent")

    # If intent is unclear, ask clarification
    if intent == "unclear":
        return "I'm not sure what you need help with. Are you asking about coding, data analysis, writing, or career advice?"

    system_prompt = SYSTEM_PROMPTS.get(intent)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content