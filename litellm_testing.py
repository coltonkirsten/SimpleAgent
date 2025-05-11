from litellm import completion
from dotenv import load_dotenv

## load environment variables from .env file
load_dotenv()

messages = [{ "content": "Please write a long poem about the meaning of life","role": "user"}]

# STATIC CALLS
# # openai call
# response = completion(model="openai/gpt-4o-mini", messages=messages)

# # anthropic call
# response2 = completion(model="anthropic/claude-3-5-haiku-latest", messages=messages)
# print(f"OPENAI:\n{response}\n\nANTHROPIC:\n{response2}")

# STREAMING CALLS
print("OPENAI:\n")
response = completion(model="openai/gpt-4o", messages=messages, stream=True)
for part in response:
    print(part.choices[0].delta.content or "", end="")

print("\n\nANTHROPIC:\n")
response = completion('anthropic/claude-3-5-haiku-latest', messages, stream=True)
for part in response:
    print(part.choices[0].delta.content or "", end="")
print("\n")