import openai

# Set your OpenAI API key
openai.api_key = 'Please place your api key, Im not giving you mine'

# Test for streaming support
try:
    stream = openai.Completion.create(model="text-davinci-003", prompt="Hello, world!", stream=True)
    print("Streaming is supported.")
except Exception as e:
    print("Streaming not supported:", e)
