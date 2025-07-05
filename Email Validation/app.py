from flask import Flask, request, jsonify, send_from_directory
from EmailValidation import validate_email, UNSUPPORTED_EXTS, parse_emails_from_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    email = data.get('email', '')
    result = validate_email(email)
    return jsonify(result)

@app.route('/validate_file', methods=['POST'])
def validate_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filename = file.filename.lower()
    for ext in UNSUPPORTED_EXTS:
        if filename.endswith(ext):
            return jsonify({'error': f'Invalid file format ({ext}). Please upload a CSV file (with emails in any column) or a JSON file (array of emails or objects with an "email" key).'}), 400
    try:
        emails, error = parse_emails_from_file(file, filename)
        if error:
            return jsonify({'error': error}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    results = [validate_email(email) for email in emails]
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)