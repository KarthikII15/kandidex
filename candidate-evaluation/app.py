from flask import Flask, request, jsonify
import os
from utils.extract_text import extract_text_from_file
import time
from utils.llama_prompt import generate_evaluation
from utils.summarizer import summarize_text
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def shorten_text(text, max_chars=1600):
    return text[:max_chars]


@app.route('/upload', methods=['POST'])
def upload_files():
    start = time.time()
    transcript = request.files.get('transcript')
    test = request.files.get('test')
    job_role = request.form.get('job_role', '')  # Default fallback
    skills_input = request.form.get('skills_to_rate', '')

    # If empty, fallback to default skills
    skills_to_rate = [s.strip() for s in skills_input.split(',')] if skills_input else [
    "Communication Skills", "Technical Knowledge", "Problem Solving"
]
    
    print("Transcript received:", transcript is not None)
    print("Test received:", test is not None)

    if not transcript or not test:
        return jsonify({'error': 'Both files are required'}), 400

    transcript_path = os.path.join(UPLOAD_FOLDER, transcript.filename)
    test_path = os.path.join(UPLOAD_FOLDER, test.filename)
    transcript.save(transcript_path)
    test.save(test_path)
    
    print("Extracting text from files...")

    # Extract text
    transcript_raw = extract_text_from_file(transcript_path)
    test_raw = extract_text_from_file(test_path)

    transcript_text = shorten_text(transcript_raw)
    test_text = shorten_text(test_raw)


    print("Transcript text:", transcript_text[:100])  # Print first 100 characters for debugging
    # Generate evaluation email
    print("Trying to summarize the context.... \n⏳ Please wait....\n")

    # email_draft = generate_evaluation(transcript_text, test_text)
    summarized_transcript = summarize_text(transcript_text)
    summarized_test = summarize_text(test_text)
    
    
    print("Generating mail... Please wait...\n⏳ Feeding into model...\n")

    email_draft = generate_evaluation(summarized_transcript, summarized_test, job_role, skills_to_rate)

    print("Email draft generated successfully!\n")
    print("Time taken for email generation:", time.time() - start)

    return jsonify({'result': email_draft})
    # return email_draft

if __name__ == '__main__':
    app.run(debug=True)
