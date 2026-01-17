#NOTE: the objective of creating this file is only to test if the api i am getting is working or not 
# 

from google import genai

client = genai.Client(api_key="GOOGLE_API_KEY")
for m in client.models.list():
    print(m.name, m.supported_generation_methods)
