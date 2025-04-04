import requests
import json

def generate_evaluation(transcript, test, job_role, skills_to_rate):
    skills_prompt = ""
    for skill in skills_to_rate:
        skills_prompt += f"   - {skill} (Rate 1-5 + comment)\n"

    prompt = f"""
You are an AI evaluator assessing a candidate for the role of **{job_role}**.

You have access to their interview transcript and problem-solving test. Based on these, please:
1. Summarize the candidate's performance in 3-4 sentences.
2. Evaluate and rate the following skills:
{skills_prompt}
3. Provide a final recommendation (Yes/No) to move to the next round with a short justification.

Format everything as a professional email with markdown-style tables.

Interview Transcript:
    {transcript}

    
    Problem Solving Test Submission:

    {test}
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
