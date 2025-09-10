from flask import Flask, jsonify
from flask import request
import io

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})

# Add /api/data POST endpoint
@app.route('/api/data', methods=['POST'])
def api_data():
    data = request.get_json()
    return jsonify({"received": data}), 200

# New endpoint for file upload
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_bytes = file.read()
    try:
        content = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return jsonify({"error": "Only text files are supported."}), 400
    # Check for printable characters
    import string
    printable = set(string.printable)
    # Count non-printable characters
    non_printable_count = sum(1 for c in content if c not in printable)
    # If more than 10% of characters are non-printable, reject
    if len(content) > 0 and (non_printable_count / len(content)) > 0.1:
        return jsonify({"error": "Only text files are supported."}), 400
    return jsonify({"content": content, "filename": file.filename}), 200

if __name__ == '__main__':
    app.run(debug=True)