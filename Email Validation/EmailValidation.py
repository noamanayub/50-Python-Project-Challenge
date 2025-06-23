import sys
import re
import dns.resolver
import smtplib
import socket
import argparse
import json
import csv
import os
from tqdm import tqdm

# Basic RFC 5322 regex
EMAIL_REGEX = re.compile(
    r"^(?P<local>[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*)$"
)
COMMON_TYPOS = {
    'gamil.com': 'gmail.com',
    'gnail.com': 'gmail.com',
    'gmil.com': 'gmail.com',
    'hotnail.com': 'hotmail.com',
    'hotmai.com': 'hotmail.com',
    'yaho.com': 'yahoo.com',
    'yahho.com': 'yahoo.com',
    'outlok.com': 'outlook.com',
    'icloud.co': 'icloud.com',
    'gmai.com': 'gmail.com',
}

# List of explicitly unsupported file extensions for uploads
UNSUPPORTED_EXTS = [
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.wav', '.mp4', '.avi', '.mov', '.mkv', '.flv', '.exe', '.dll', '.bat', '.sh', '.psd', '.ai', '.eps', '.jsonl', '.xml', '.yaml', '.yml', '.svc', '.bin', '.apk', '.csvs', '.html', '.htm', '.css', '.js', '.ts', '.c', '.cpp', '.java', '.php', '.asp', '.aspx', '.jsp', '.swift', '.go', '.rs', '.pl', '.rb', '.m', '.kt', '.dart', '.lua', '.r', '.sas', '.sql', '.db', '.dbf', '.sqlite', '.md', '.log', '.out', '.bak', '.tmp', '.dat', '.sav', '.sketch', '.indd', '.xd', '.fla', '.swf', '.dwg', '.dxf', '.stl', '.obj', '.3ds', '.blend', '.fbx', '.scad', '.step', '.iges', '.sldprt', '.sldasm', '.prt', '.asm', '.iges', '.step', '.iges', '.sldprt', '.sldasm', '.prt', '.asm'
]


def suggest(email):
    m = EMAIL_REGEX.match(email)
    if not m:
        return ''
    d = m.group('domain').lower()
    if d in COMMON_TYPOS:
        return f"{m.group('local')}@{COMMON_TYPOS[d]}"
    return ''


def is_valid_syntax(email):
    return bool(EMAIL_REGEX.match(email))


def has_mx(domain):
    try:
        return bool(dns.resolver.resolve(domain, 'MX'))
    except Exception:
        return False


def verify_smtp(email, sender='validator@example.com'):
    try:
        mx = str(dns.resolver.resolve(email.split('@')[1], 'MX')[0].exchange)
        server = smtplib.SMTP(timeout=10)
        server.connect(mx)
        server.helo(socket.gethostname())
        server.mail(sender)
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False


def load_list(path):
    items = set()
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                d = line.strip().lower()
                if d:
                    items.add(d)
    return items


def generate_report(results, report_type, out_path):
    if report_type == 'html':
        lines = ['<html><body><table border="1" cellpadding="5"><tr><th>Email</th><th>Status</th><th>Syntax</th><th>MX</th><th>SMTP</th><th>Suggestion</th></tr>']
        for r in results:
            lines.append(
                f"<tr><td>{r['email']}</td><td>{'✔' if r['valid'] else '✘'}</td>"
                f"<td>{r['syntax']}</td><td>{r['domain']}</td><td>{r['smtp']}</td><td>{r['suggestion'] or ''}</td></tr>"
            )
        lines.append('</table></body></html>')
        with open(out_path, 'w') as f:
            f.write('\n'.join(lines))
    elif report_type == 'md':
        header = '| Email | Status | Syntax | MX | SMTP | Suggestion |'
        sep = '|---|:---:|:---:|:---:|:---:|---|'
        lines = [header, sep]
        for r in results:
            lines.append(
                f"| {r['email']} | {'✔' if r['valid'] else '✘'} | {r['syntax']} | {r['domain']} | {r['smtp']} | {r['suggestion']} |"
            )
        with open(out_path, 'w') as f:
            f.write('\n'.join(lines))


def validate_email(email, smtp_check=False, whitelist=None, blacklist=None):
    """
    Validate a single email address and return a result dict.
    """
    r = {'email': email, 'syntax': False, 'domain': False, 'smtp': None, 'valid': False, 'suggestion': ''}
    if '@' in email:
        dom = email.split('@')[1].lower()
    else:
        dom = ''
    if whitelist and dom not in whitelist:
        r['valid'] = False
    elif blacklist and dom in blacklist:
        r['valid'] = False
    else:
        r['syntax'] = is_valid_syntax(email)
        if r['syntax']:
            if dom in COMMON_TYPOS:
                r['suggestion'] = suggest(email)
            else:
                r['domain'] = has_mx(dom)
                if smtp_check and r['domain']:
                    r['smtp'] = verify_smtp(email)
                r['valid'] = r['domain'] and (r['smtp'] is not False)
                if not r['valid']:
                    r['suggestion'] = suggest(email)
    return r


def parse_emails_from_file(file, filename):
    import csv, io, json
    emails = []
    error = None
    if filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode('utf-8'))
            reader = csv.reader(stream)
            for row in reader:
                for item in row:
                    item = item.strip()
                    if '@' in item:
                        emails.append(item)
        except Exception:
            error = 'Invalid CSV file. Please upload a valid CSV file with emails.'
    elif filename.endswith('.json'):
        try:
            data = json.load(file.stream)
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, str) and '@' in entry:
                        emails.append(entry)
                    elif isinstance(entry, dict) and 'email' in entry:
                        emails.append(entry['email'])
        except Exception:
            error = 'Invalid JSON file. Please upload a valid JSON array of emails or objects with an "email" key.'
    else:
        error = 'Invalid file format. Please upload a CSV file (with emails in any column) or a JSON file (array of emails or objects with an "email" key).'
    return emails, error


def main():
    p = argparse.ArgumentParser(description='Email Validation Tool')
    p.add_argument('input', nargs='+', help='Emails or file path')
    p.add_argument('--smtp', action='store_true', help='Enable SMTP verify')
    p.add_argument('--blacklist-file', help='Path to domain blacklist file')
    p.add_argument('--whitelist-file', help='Path to domain whitelist file')
    p.add_argument('--format', choices=['json', 'csv', 'text'], default='text', help='Output format')
    p.add_argument('--report', choices=['html', 'md'], help='Generate HTML/Markdown report')
    args = p.parse_args()

    blacklist = load_list(args.blacklist_file) if args.blacklist_file else set()
    whitelist = load_list(args.whitelist_file) if args.whitelist_file else set()

    emails = []
    for src in args.input:
        if os.path.isfile(src):
            with open(src) as f:
                emails.extend([l.strip() for l in f if l.strip()])
        else:
            emails.append(src)

    results = []
    for email in tqdm(emails, desc='Validating'):
        r = {'email': email, 'syntax': False, 'domain': False, 'smtp': None, 'valid': False, 'suggestion': ''}
        if '@' in email:
            dom = email.split('@')[1].lower()
        else:
            dom = ''
        if whitelist and dom not in whitelist:
            r['valid'] = False
        elif blacklist and dom in blacklist:
            r['valid'] = False
        else:
            r['syntax'] = is_valid_syntax(email)
            if r['syntax']:
                if dom in COMMON_TYPOS:
                    r['suggestion'] = suggest(email)
                else:
                    r['domain'] = has_mx(dom)
                    if args.smtp and r['domain']:
                        r['smtp'] = verify_smtp(email)
                    r['valid'] = r['domain'] and (r['smtp'] is not False)
                    if not r['valid']:
                        r['suggestion'] = suggest(email)
        results.append(r)

    # Output
    if args.format == 'json':
        print(json.dumps(results, indent=2))
    elif args.format == 'csv':
        w = csv.writer(sys.stdout)
        w.writerow(['email','valid','syntax','domain','smtp','suggestion'])
        for r in results:
            w.writerow([r['email'], r['valid'], r['syntax'], r['domain'], r['smtp'], r['suggestion']])
    else:
        # plain text
        for i,r in enumerate(results,1):
            print(f"{i}) {r['email']} -> {'VALID' if r['valid'] else 'INVALID'}")
            print(f"   Syntax: {r['syntax']}  MX: {r['domain']}  SMTP: {r['smtp']}")
            if r['suggestion']:
                print(f"   Suggestion: {r['suggestion']}")
            print()

    # Report file
    if args.report:
        out = f"report.{args.report}"
        generate_report(results, args.report, out)
        print(f"Report generated: {out}")

if __name__ == '__main__':
    main()