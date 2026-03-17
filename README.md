## Build an LLM-Powered Prompt Router for Intent Classification

## Project Overview

This project implements an AI prompt routing system that intelligently directs user requests to specialized AI personas based on the detected intent of the message. Instead of using a single large prompt to handle all types of requests, the system first classifies the user’s intent and then routes the request to a specialized expert prompt designed for that task.

The application demonstrates a practical production design pattern known as **intent-based prompt routing**, which is commonly used in modern AI applications to improve response accuracy and maintainability. The system uses a two-step architecture: first classifying the intent of the user message, and then generating the final response using a specialized system prompt.

This project is implemented in **Python** and uses the **Groq API with the Llama model** to perform both classification and response generation. The application is containerized using **Docker**, allowing the system to run consistently across different environments.

---

## System Architecture

The system follows a two-step AI routing architecture.

1. **Intent Classification**
   - The user's message is first analyzed by a lightweight classifier prompt.
   - The classifier determines the most likely intent category.
   - The classifier returns a structured JSON response containing the detected intent and a confidence score.

2. **Prompt Routing and Response Generation**
   - Based on the classified intent, the system selects a specialized expert persona.
   - The user message and expert system prompt are sent to the LLM to generate the final response.

This architecture improves performance and accuracy because each expert prompt is optimized for a specific task instead of attempting to solve all tasks with a single prompt.

---

## Supported Intents

The system currently supports the following intents:

| Intent | Description |
|------|-------------|
| code | Programming questions, debugging, software development |
| data | Statistical analysis, datasets, averages, SQL queries |
| writing | Feedback on text clarity, grammar, tone, and structure |
| career | Career advice, resumes, interview preparation |
| unclear | Messages that do not clearly belong to any supported category |

If the intent is classified as **unclear**, the system does not attempt to answer the question directly and instead asks the user for clarification.

---

## Expert System Prompts

The system defines four expert personas that are used to generate responses:

### Code Expert
Provides programming solutions, code examples, debugging help, and best practices for software development.

### Data Analyst
Interprets numerical information and datasets using statistical concepts such as averages, trends, and distributions.

### Writing Coach
Provides feedback on grammar, tone, clarity, and writing structure without rewriting the user's content.

### Career Advisor
Offers practical career guidance and asks clarifying questions before providing advice.

All system prompts are stored in a configuration structure (`prompts.py`) rather than being hardcoded inside business logic.

---

## Core Functions

### classify_intent(message: str)

This function performs the first LLM call to determine the user's intent.

Steps performed:

1. Sends a classification prompt to the LLM.
2. The model returns a JSON response containing:
   ```json
   {
     "intent": "string",
     "confidence": float
   }
   ```
3. The JSON response is parsed into a Python dictionary.
4. If parsing fails or the response is malformed, the function safely returns:

```json
{
  "intent": "unclear",
  "confidence": 0.0
}
```

This ensures the system never crashes due to malformed model responses.

---

### route_and_respond(message: str, intent: dict)

This function generates the final response.

Steps performed:

1. Reads the classified intent from the classifier output.
2. Selects the corresponding expert system prompt.
3. Sends the system prompt and user message to the LLM.
4. Returns the generated response.

If the intent is **unclear**, the system returns a clarification message instead of routing to an expert.

---

## Logging

For observability and debugging, the application logs every request.

Logs are stored in a **JSON Lines file** named:

```
route_log.jsonl
```

Each line represents a single request and contains:

```json
{
  "intent": "code",
  "confidence": 0.95,
  "user_message": "how do I sort a list in python",
  "final_response": "..."
}
```

This logging system allows the routing behavior of the application to be inspected and analyzed.

---

## Project Structure

The repository is organized as follows:

```
ai-prompt-router
│
├── classifier.py
├── router.py
├── prompts.py
├── logger.py
├── main.py
├── test_messages.py
│
├── Dockerfile
├── docker-compose.yml
│
├── .env.example
├── .gitignore
│
├── route_log.jsonl
└── README.md
```

### File Descriptions

**classifier.py**

Implements the `classify_intent()` function which performs intent classification using the LLM.

**router.py**

Contains the `route_and_respond()` function responsible for selecting the correct expert persona and generating responses.

**prompts.py**

Stores all expert system prompts in a dictionary keyed by intent label.

**logger.py**

Handles structured logging of routing decisions to `route_log.jsonl`.

**main.py**

Provides the command-line interface for interacting with the system.

**test_messages.py**

Contains a set of test cases used to validate the routing behavior.

**Dockerfile**

Defines the container environment used to run the application.

**docker-compose.yml**

Simplifies container execution and allows the application to be started with a single command.

---

## Environment Variables

The application requires an API key for the Groq LLM service.

Create a `.env` file based on `.env.example`.

Example:

```
GROQ_API_KEY=your_api_key_here
```

The `.env` file is intentionally excluded from version control for security reasons.

---

## Running the Application

### Run Locally

Install dependencies:

```
pip install groq python-dotenv
```

Run the program:

```
python main.py
```

You will then be prompted to enter a message.

---

### Run Tests

To test the classifier behavior:

```
python test_messages.py
```

This script runs several test cases covering:

- normal inputs
- ambiguous messages
- multiple intents
- typos
- unsupported requests

---

## Docker Setup

The application is containerized to ensure consistent execution.

Build the Docker image:

```
docker build -t ai-router .
```

Run the container:

```
docker run -it --env-file .env ai-router
```

---

### Docker Compose

The project also includes a Docker Compose configuration.

Run the application:

```
docker compose up --build
```

Stop the container:

```
docker compose down
```

---

## Design Decisions

Several design decisions were made to improve reliability and maintainability.

**Prompt Routing**

Separating intent classification from response generation improves accuracy compared to a single large prompt.

**Structured JSON Output**

The classifier always returns structured JSON to simplify parsing and routing logic.

**Error Handling**

Malformed model outputs are safely handled by falling back to the `unclear` intent.

**Logging**

The system logs every routing decision to enable debugging and analysis.

**Containerization**

Docker ensures that the application runs consistently across different systems.

---

## Testing Strategy

The project includes a test script that validates the routing behavior across multiple scenarios including:

- programming questions
- data analysis requests
- writing feedback
- career advice
- greetings
- ambiguous messages
- creative writing requests

This helps ensure that the classifier and router behave as expected.

---

## Conclusion

This project demonstrates how to build an intent-based AI routing system using prompt engineering techniques and structured LLM outputs. The architecture separates intent detection from response generation, allowing the system to route requests to specialized expert personas.

By combining prompt engineering, structured outputs, and containerized deployment, this application provides a practical example of how modern AI systems can be designed for flexibility, reliability, and scalability.