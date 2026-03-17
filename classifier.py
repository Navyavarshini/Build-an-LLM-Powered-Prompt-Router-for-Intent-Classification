import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_intent(message: str):

    classifier_prompt = """
            You are an intent classification system.

            Classify the user message into ONE of these intents:

            code
            data
            writing
            career
            unclear

            Definitions:

            code → programming, debugging, APIs, frameworks, software development questions

            data → statistics, averages, datasets, SQL, spreadsheets, analysis

            writing → feedback on existing text (grammar, clarity, tone, rewriting)

            career → resumes, job advice, interviews, career decisions

            unclear → greetings, creative writing requests (poems, stories),
            or requests outside the categories above.

            Examples:

            User: how do I sort a list in python
            Output: {"intent":"code","confidence":0.9}

            User: how do I create a REST API in python
            Output: {"intent":"code","confidence":0.9}

            User: calculate the average of 5, 10, 15
            Output: {"intent":"data","confidence":0.9}

            User: my writing sounds awkward
            Output: {"intent":"writing","confidence":0.9}

            User: write a poem about clouds
            Output: {"intent":"unclear","confidence":0.9}

            Respond ONLY with JSON:
            {
            "intent": "...",
            "confidence": 0.0-1.0
            }
"""
    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": classifier_prompt},
                {"role": "user", "content": message}
            ]
        )

        result = response.choices[0].message.content

        parsed = json.loads(result)

        allowed_intents = ["code", "data", "writing", "career", "unclear"]

        intent = parsed.get("intent")
        confidence = parsed.get("confidence", 0)

        # if intent not allowed OR confidence too low → unclear
        if intent not in allowed_intents or confidence < 0.8:
            return {
                "intent": "unclear",
                "confidence": 0.0
            }

        return parsed

    except Exception:

        return {
            "intent": "unclear",
            "confidence": 0.0
        }