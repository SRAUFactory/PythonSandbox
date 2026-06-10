import requests
import sys

URL = "http://localhost:11434/v1/chat/completions"
MODEL = "gemma4:e4b"

PROMPT = """10段の階段があります。
1歩で1段または2段を上ることができます。
ただし、1歩で2段上がれるのは3回までです。
では、ちょうど10段目に到達する上り方は何通りありますか?"""

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ollama"
}

data = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "あなたは優秀なAIアシスタントです。"},
        {"role": "user", "content": PROMPT}
    ],
    "temperature": 0.7
}

response = requests.post(URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print("Error:", response.status_code)
    print(response.text)
