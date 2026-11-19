
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenRouter configuration
MODEL_NAME = "openrouter/free"

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Check your .env file."
    )

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    timeout=30.0,
    max_retries=0
)


def ask_model(prompt: str) -> str:
    """Send a prompt to an AI model through OpenRouter."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    if not result:
        raise RuntimeError("The AI returned an empty response.")

    return result


if __name__ == "__main__":
    print("Testing CodePilot with OpenRouter...")

    result = ask_model(
        "Explain Python functions in two simple sentences."
    )

    print("\nAI response:\n")
    print(result)
