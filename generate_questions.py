import requests

# Load Hugging Face API key
with open("huggingface_key.txt", "r") as f:
    hf_token = f.read().strip()

# Load resume and JD text
with open("resume_text.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

with open("job_text.txt", "r", encoding="utf-8") as f:
    job_text = f.read()

# Define prompt
prompt = f"""
You are an AI interview coach.

Given the following resume and job description, generate:
1. 5 technical interview questions based on the job requirements.
2. 3 behavioral questions based on the resume.
3. Suggestions on what the candidate should prepare more based on the gap.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""

# Send to Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {
    "Authorization": f"Bearer {hf_token}"
}

payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 500,
        "temperature": 0.7,
        "return_full_text": False
    }
}

print("\n⏳ Generating AI interview questions...\n")

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        print("🎤 Interview Questions and Feedback:\n")
        print(result[0]["generated_text"])
    else:
        print("⚠️ Response format unexpected:", result)
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
