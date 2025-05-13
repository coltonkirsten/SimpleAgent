from agent.litellm_interface import LitellmInterface
import base64
from PIL import Image
import io

Tools = {
  "tools": [
    "tools.util_tools"
  ]
}

# system_message = "You are a programming assistant. Remember when calling tools all code must be written in the /Users/coltonkirsten/Desktop/Projects/SimpleAgentFramework/ai_playground/ directory. When the user asks for any code just directly call the tool do not provide the user any code. If the tool call fails, just tell the user there was an error and perform no further actions."
system_message = "You are a helpful assistant."

model = "anthropic/claude-3-5-haiku-latest"
# model = "openai/gpt-4.1"
# model = "openai/o4-mini"

bot = LitellmInterface(
    model=model,
    system_role=system_message,
    stream=True,
    tools=Tools
)

# Start conversation loop
print("-" * 50)
print("Welcome to the homework agent")
print("Model: ", model)
print("\nType 'exit', 'quit', or 'bye' to end the conversation.")
print("-" * 50)

# Load the image, convert to JPEG, then encode to base64
img = Image.open("image.png")
buffer = io.BytesIO()
img.convert('RGB').save(buffer, format='JPEG')
buffer.seek(0)
base64_image = base64.b64encode(buffer.read()).decode("utf-8")

while True:
    # Get user input
    user_input = input("\nYou: ")
    
    # Check for exit commands
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nGoodbye!")
        break
    
    # Get response from the AI
    print("\nAssistant: ", end="", flush=True)
    
    response = bot.prompt(user_input,image=base64_image)
    
    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")
