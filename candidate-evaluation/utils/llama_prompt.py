import requests

def generate_evaluation(transcript, test):
    prompt = f"""
You are an HR evaluator. Based on the following interview transcript and problem-solving test, generate a candidate evaluation email.

Interview Transcript:
{transcript}

Problem-Solving Test:
{test}

Evaluate:
- Communication Skills (1-10)
- Technical Skills (1-10)
- Problem Solving (1-10)
- Strengths
- Weaknesses
- Final Verdict (Short paragraph)

Format the output as a professional email.
"""
    try:
        # Send the prompt to the LLAMA3 API for evaluation generation
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "llama3",
                  "prompt": prompt,
                  "stream": True,
                  "options": {"num_predict": 250}
                  }
        )
        
        output = ""
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk = eval(line.decode("utf-8"))["response"]
                    output += chunk
            return output
        else:
            return "Failed to generate evaluation from LLAMA3."
        
        # response.raise_for_status()  # Raise an error for bad responses
        # return response.json()['response']
    
    except requests.exceptions.RequestException as e:
        print(f"Ollama request failed: {e}")
        return "Error: LLM service is currently unavailable. Please try again later."

