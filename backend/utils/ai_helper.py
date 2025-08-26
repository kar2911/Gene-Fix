import requests
import json
from google import genai

def get_ai_simulation_message(prompt):
    client = genai.Client(api_key="AIzaSyDmPXyDJoLknUu1HrpIlIGf0RtCYOEeMr0")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

# def get_ai_simulation_message(prompt):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": "Bearer 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",  # Replace with your actual key
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "model": "deepseek/deepseek-chat-v3-0324:free",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(payload))

#     # Check if the response is successful
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         raise Exception(f"API call failed with status {response.status_code}: {response.text}")
