from classifier import classify_intent
from router import route_and_respond
from logger import log_route

message = input("Enter your message: ")

# -------- Manual Override --------
override_intents = ["code", "data", "writing", "career"]

if message.startswith("@"):
    parts = message.split(" ", 1)
    tag = parts[0][1:]

    if tag in override_intents:
        intent_data = {
            "intent": tag,
            "confidence": 1.0
        }

        # remove the @tag from message
        if len(parts) > 1:
            message = parts[1]

    else:
        intent_data = classify_intent(message)

else:
    intent_data = classify_intent(message)

# -------- Generate Response --------
response = route_and_respond(message, intent_data)

print("\n-----------------------------------")
print("User Message:", message)
print("Intent:", intent_data["intent"])
print("Confidence:", intent_data["confidence"])
print("-----------------------------------")

print("\nResponse:\n")
print(response)

# -------- Logging --------
log_route(
    intent_data["intent"],
    intent_data["confidence"],
    message,
    response
)