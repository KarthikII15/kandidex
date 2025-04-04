from flask import Flask, request, jsonify
import os
from utils.extract_text import extract_text_from_file
import time
from utils.llama_prompt import generate_evaluation

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def shorten_text(text, max_chars=2000):
    return text[:max_chars]


@app.route('/upload', methods=['POST'])
def upload_files():
    start = time.time()
    transcript = request.files.get('transcript')
    test = request.files.get('test')
    
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
    print("generating mail..... \n Please wait.....\n ")
    email_draft = generate_evaluation(transcript_text, test_text)
    
    print("⏱️ Time taken:", time.time() - start)

    return jsonify({'email': email_draft})

if __name__ == '__main__':
    app.run(debug=True)
