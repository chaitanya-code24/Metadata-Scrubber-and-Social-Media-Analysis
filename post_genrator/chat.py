import requests

API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
text="ai race"
output = query({
    "inputs": f"create a twiter post on '{text}' ",
})

