from agent.litellm_interface import LitellmInterface

Tools = {
  "tools": [
    "tools.weather_tool",
    "tools.light_control_tool",
    "tools.util_tools",
    "tools.web_search_tool",
  ]
}

system_message = "You are a total chiller. respond super duper chill and like a total bro."

model = "anthropic/claude-3-5-haiku-latest"
model = "openai/gpt-4o-mini"

bot = LitellmInterface(
    model=model,
    system_role=system_message,
    stream=True,
    tools=Tools
)

# Start conversation loop
print("-" * 50)
print("Welcome to the agent")
print("Model: ", model)
print("\nType 'exit', 'quit', or 'bye' to end the conversation.")
print("-" * 50)

while True:
    # Get user input
    user_input = input("\nYou: ")
    
    # Check for exit commands
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nGoodbye!")
        break
    
    # Get response from the AI
    print("\nAssistant: ", end="", flush=True)
    
    response = bot.prompt(user_input)
    
    for chunk in response:
        print(chunk, end="", flush=True)
    print("\n")
