from classifier import classify_intent

test_messages = [

    # very short message
    "hi",

    # greeting
    "hello",

    # multiple intents
    "I need help writing code and fixing my resume",

    # typo message
    "fxi thsi bug pls: for i in range(10) print(i)",

    # long message
    """I am preparing for a technical interview and I want to understand
    how sorting algorithms work in Python and also how they compare
    with SQL sorting methods""",

    # unrelated request
    "write a poem about clouds",

    # normal code request
    "how do I create a REST API in python",

    # writing improvement
    "my boss says my writing is too verbose",

    # data question
    "calculate the average of 5, 10, 15, 20"
]

for msg in test_messages:
    print("\n===============================")
    print("Message:", msg)

    result = classify_intent(msg)

    print("Intent:", result["intent"])
    print("Confidence:", result["confidence"])