import requests
import json
import ollama

def generate_evaluation(transcript, test, job_role, skills_to_rate):
    skills_prompt = ""
    for skill in skills_to_rate:
        skills_prompt += f"   - {skill} (Rate 1-5 + comment)\n"

    prompt = f"""
Draft a short formal email for HR Team by Evaluating the candidate as a interviewer for [ROLE] based on:
-Interview Transcript:
    {transcript}
- Problem Solving Test Submission:
    {test}
- Job Role:
    {job_role}
Points to be included in the email:
- Candidate Name
- Summarize strengths and weaknesses (max 100 words)
- Strictly Rate these skills: [SKILLS] and give comments on each skill. 
- If skills are empty, rate the candidate on the relavent skills to the role.
- Striclth Rate each skill from 1 to 5, with 1 being the lowest and 5 being the highest.
- Give a final recommendation: Strong Hire / Hire / Hold / Reject based on the performance and skills
- Add justification for the recommendation (max 100 words)
    """
    
    response = ollama.chat(
    model='llama3:8b',
    messages=[{"role": "user", "content": prompt}],
    options={
        "temperature": 0.3,      # More focused answers
        "top_p": 0.9,            # Reduces randomness
        "num_predict": 512       # Limits max tokens to speed up response
    }
)
    
    result = response['message']['content']
    return result



    # response = requests.post(
    #     'http://localhost:11434/api/generate',
    #     # json={"model": "mistral", "prompt": prompt, "stream": True},
    #     json={"model": "llama3:8b", "prompt": prompt, "stream": True},
    #     stream=True
    # )

    # output = ""
    # if response.status_code == 200:
    #     for line in response.iter_lines():
    #         if line:
    #             try:
    #                 data = json.loads(line.decode("utf-8"))
    #                 output += data.get("response", "")
    #             except json.JSONDecodeError as e:
    #                 print(f"JSON decode error: {e}")
    #     return output
    # else:
    #     return "Failed to generate evaluation from LLAMA3."
