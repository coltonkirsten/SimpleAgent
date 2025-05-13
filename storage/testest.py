from litellm import get_supported_openai_params

response = get_supported_openai_params(model="anthropic/claude-3-5-haiku-latest")

print(response)