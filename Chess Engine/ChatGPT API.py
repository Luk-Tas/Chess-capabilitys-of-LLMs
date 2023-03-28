import openai, os

openai.api_key_path = r'C:\Users\Lukas\Desktop\Ordner\OpenAI\Key2.txt'

response = openai.Completion.create(model="gpt-3.5-turbo", prompt="Say this is a test", temperature=0, max_tokens=7)
print(response)
