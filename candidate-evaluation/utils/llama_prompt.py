import requests
import json

def generate_evaluation(transcript, test, job_role, skills_to_rate):
    skills_prompt = ""
    for skill in skills_to_rate:
        skills_prompt += f"   - {skill} (Rate 1-5 + comment)\n"

    prompt = f"""
Evaluate the candidate for [ROLE] based on:
- Interview Transcript
- Test Performance

Rate these skills: [SKILLS]  
Summarize performance (max 150 words)  
Give a final recommendation  
Then draft a short formal email for HR with your assessment.

Interview Transcript:
    {transcript}

    
    Problem Solving Test Submission:

    {test}
    """

    response = requests.post(
        'http://localhost:11434/api/generate',
        # json={"model": "mistral", "prompt": prompt, "stream": True},
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
