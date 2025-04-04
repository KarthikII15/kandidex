import requests
import json

def generate_evaluation(transcript, test):
    prompt = f"""
Evaluate the candidate using the interview transcript and test content below.

Transcript:
{transcript}

Test:
{test}

Output an email containing:
- Ratings (for relavent skills) [1–5]
- Strengths & Weaknesses
- Final Summary Verdict
- Recommendation (Hire/No Hire)
Format the output as a professional email to HR Team.
"""

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={"model": "llama3:8b", "prompt": prompt, "stream": True},
        stream=True
    )

    output = ""
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    output += data.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
        return output
    else:
        return "Failed to generate evaluation from LLAMA3."
