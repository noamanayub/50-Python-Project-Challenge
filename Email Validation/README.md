# Email Validation Web App

A modern Python web application for validating email addresses individually or in bulk (CSV/JSON upload). Features include syntax and MX checks, typo suggestions, blacklist/whitelist, progress bar, CSV download, and more.

## Features
- Validate single emails or upload CSV/JSON files for bulk validation
- Progress bar for file processing
- Download results as CSV
- Copy all valid emails to clipboard
- See total, valid, and invalid counts
- Typo suggestions for common domains
- Blacklist/whitelist support (CLI)
- Beautiful, responsive UI

## Usage

### 1. Web App
1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Run the Flask app:
   ```
   python app.py
   ```
3. Open your browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
4. Enter an email or upload a CSV/JSON file to validate.

### 2. Command Line
Validate emails from the terminal:
```bash
python EmailValidation.py test@example.com
python EmailValidation.py emails.csv --format json
python EmailValidation.py emails.json --format csv
```

#### Options
- `--smtp` : Enable SMTP verification (slower, more accurate)
- `--blacklist-file path.txt` : Blacklist domains
- `--whitelist-file path.txt` : Whitelist domains
- `--format [json|csv|text]` : Output format
- `--report [html|md]` : Generate HTML/Markdown report

### File Upload Formats
- **CSV:** Any column, any row containing an email address
- **JSON:** Array of emails or array of objects with an `email` key

### Not Supported
- Image, document, and code files (see `UNSUPPORTED_EXTS` in `EmailValidation.py`)

## Project Structure
- `app.py` - Flask web backend
- `EmailValidation.py` - Core validation logic and CLI
- `index.html` - Web frontend
- `style.css` - Stylesheet
- `requirements.txt` - Python dependencies

## Requirements
- Python 3.8+
- See `requirements.txt`

