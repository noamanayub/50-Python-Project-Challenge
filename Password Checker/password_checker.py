#!/usr/bin/env python3
"""
🔐 Advanced Password Strength Checker GUI v2.0
Enhanced by Noaman Ayub
A modern GUI application for comprehensive password analysis

Features:
- Real-time password strength visualization
- Interactive strength meter
- Breach database checking simulation
- Password generation with customization
- Security compliance checking
- Modern, user-friendly interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
import math
import random
import string
import hashlib
import time
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class PasswordCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Password Strength Checker v2.0 - Enhanced by Noaman Ayub")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='#ecf0f1')
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#2c3e50', foreground='#3498db')
        self.style.configure('Result.TLabel', font=('Arial', 10), background='#2c3e50', foreground='#ecf0f1')
        self.style.configure('Success.TLabel', font=('Arial', 10), background='#2c3e50', foreground='#27ae60')
        self.style.configure('Warning.TLabel', font=('Arial', 10), background='#2c3e50', foreground='#e74c3c')
        
        # Initialize password checker logic
        self.init_checker_logic()
        
        # Create GUI
        self.create_widgets()
        
        # Bind real-time checking
        self.password_var.trace('w', self.on_password_change)
    
    def init_checker_logic(self):
        """Initialize password checking logic"""
        self.common_passwords = {
            'english': [
                'password', 'admin', 'welcome', 'login', 'master', 'secret',
                'qwerty', '123456', 'letmein', 'monkey', 'dragon', 'princess',
                'football', 'baseball', 'superman', 'michael', 'jordan'
            ],
            'patterns': [
                r'(.)\1{2,}',  # Repeated characters
                r'(012|123|234|345|456|567|678|789|890)',  # Sequential numbers
                r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
                r'(qwe|wer|ert|rty|tyu|yui|uio|iop|asd|sdf|dfg|fgh|ghj|hjk|jkl|zxc|xcv|cvb|vbn|bnm)',  # Keyboard patterns
            ]
        }
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Advanced Password Strength Checker v2.0", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="Enhanced by Noaman Ayub", style='Heading.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Password Analysis Tab
        self.create_analysis_tab(notebook)
        
        # Password Generator Tab
        self.create_generator_tab(notebook)
        
        # Security Tips Tab
        self.create_tips_tab(notebook)
        
        # Batch Analysis Tab
        self.create_batch_tab(notebook)
    
    def create_analysis_tab(self, notebook):
        """Create password analysis tab"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="🔍 Password Analysis")
        
        # Password input section
        input_frame = ttk.LabelFrame(analysis_frame, text="Password Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter password to analyze:", style='Heading.TLabel').pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, font=('Arial', 12), width=50, show='*')
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Show/Hide password button
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.show_password_var = tk.BooleanVar()
        show_check = ttk.Checkbutton(button_frame, text="Show password", variable=self.show_password_var, command=self.toggle_password_visibility)
        show_check.pack(side=tk.LEFT)
        
        analyze_btn = ttk.Button(button_frame, text="🔍 Analyze", command=self.analyze_password_gui)
        analyze_btn.pack(side=tk.RIGHT)
        
        # Strength meter
        meter_frame = ttk.LabelFrame(analysis_frame, text="Strength Meter", padding=10)
        meter_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.strength_var = tk.StringVar(value="Enter a password")
        strength_label = ttk.Label(meter_frame, textvariable=self.strength_var, style='Heading.TLabel')
        strength_label.pack()
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(meter_frame, variable=self.progress_var, maximum=10, length=400)
        self.progress_bar.pack(pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, font=('Consolas', 10), 
                                                     bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1')
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_generator_tab(self, notebook):
        """Create password generator tab"""
        generator_frame = ttk.Frame(notebook)
        notebook.add(generator_frame, text="🎲 Password Generator")
        
        # Generator options
        options_frame = ttk.LabelFrame(generator_frame, text="Generation Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Length setting
        length_frame = ttk.Frame(options_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text="Password Length:", style='Heading.TLabel').pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=16)
        length_spin = ttk.Spinbox(length_frame, from_=8, to=50, textvariable=self.length_var, width=10)
        length_spin.pack(side=tk.RIGHT)
        
        # Character options
        char_frame = ttk.Frame(options_frame)
        char_frame.pack(fill=tk.X, pady=5)
        
        self.include_upper_var = tk.BooleanVar(value=True)
        self.include_lower_var = tk.BooleanVar(value=True)
        self.include_digits_var = tk.BooleanVar(value=True)
        self.include_symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(char_frame, text="Uppercase (A-Z)", variable=self.include_upper_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Lowercase (a-z)", variable=self.include_lower_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Digits (0-9)", variable=self.include_digits_var).pack(anchor=tk.W)
        ttk.Checkbutton(char_frame, text="Symbols (!@#$...)", variable=self.include_symbols_var).pack(anchor=tk.W)
        
        # Generate button
        generate_btn = ttk.Button(options_frame, text="🎲 Generate Password", command=self.generate_password_gui)
        generate_btn.pack(pady=10)
        
        # Generated password display
        result_frame = ttk.LabelFrame(generator_frame, text="Generated Password", padding=10)
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.generated_password_var = tk.StringVar()
        password_display = ttk.Entry(result_frame, textvariable=self.generated_password_var, 
                                   font=('Arial', 14, 'bold'), state='readonly')
        password_display.pack(fill=tk.X, pady=5)
        
        button_frame2 = ttk.Frame(result_frame)
        button_frame2.pack(fill=tk.X, pady=5)
        
        copy_btn = ttk.Button(button_frame2, text="📋 Copy", command=self.copy_password)
        copy_btn.pack(side=tk.LEFT)
        
        analyze_gen_btn = ttk.Button(button_frame2, text="🔍 Analyze", command=self.analyze_generated)
        analyze_gen_btn.pack(side=tk.RIGHT)
        
        # Multiple passwords generation
        multi_frame = ttk.LabelFrame(generator_frame, text="Batch Generation", padding=10)
        multi_frame.pack(fill=tk.BOTH, expand=True)
        
        multi_button_frame = ttk.Frame(multi_frame)
        multi_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(multi_button_frame, text="Generate multiple passwords:", style='Heading.TLabel').pack(side=tk.LEFT)
        
        self.multi_count_var = tk.IntVar(value=5)
        count_spin = ttk.Spinbox(multi_button_frame, from_=2, to=20, textvariable=self.multi_count_var, width=5)
        count_spin.pack(side=tk.RIGHT, padx=(5, 0))
        
        multi_gen_btn = ttk.Button(multi_button_frame, text="🎲 Generate Multiple", command=self.generate_multiple_passwords)
        multi_gen_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        self.multi_results_text = scrolledtext.ScrolledText(multi_frame, height=10, font=('Consolas', 10),
                                                           bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1')
        self.multi_results_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def create_tips_tab(self, notebook):
        """Create security tips tab"""
        tips_frame = ttk.Frame(notebook)
        notebook.add(tips_frame, text="📚 Security Tips")
        
        tips_text = scrolledtext.ScrolledText(tips_frame, font=('Arial', 11), bg='#34495e', 
                                             fg='#ecf0f1', insertbackground='#ecf0f1')
        tips_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tips_content = """
🛡️ PASSWORD SECURITY BEST PRACTICES
==========================================

🔑 LENGTH AND COMPLEXITY
• Use at least 12 characters (longer is better)
• Mix uppercase and lowercase letters
• Include numbers and special characters
• Avoid predictable patterns and sequences

🚫 WHAT TO AVOID
• Personal information (names, birthdays, addresses)
• Common words and phrases
• Keyboard patterns (qwerty, 123456)
• Repeated characters (aaa, 111)
• Simple substitutions (@ for a, 3 for e)

🔄 PASSWORD MANAGEMENT
• Use unique passwords for each account
• Change passwords every 3-6 months
• Don't reuse old passwords
• Use a reputable password manager
• Enable two-factor authentication (2FA)

🕵️ SECURITY MONITORING
• Regularly check if your accounts have been breached
• Monitor your accounts for suspicious activity
• Keep your devices and browsers updated
• Be cautious of phishing emails and fake websites

🔐 ADVANCED TIPS
• Consider using passphrases with random words
• Use password generators for maximum security
• Don't store passwords in browsers on shared devices
• Backup your password manager data securely

💡 PASSPHRASE EXAMPLE
Instead of: P@ssw0rd123!
Try: Elephant-Bicycle-Rainbow-Coffee-7!

The passphrase is longer, easier to remember, and much more secure!

🎯 COMPLIANCE STANDARDS
• NIST: Minimum 8 characters, recommended 12+
• PCI DSS: 8+ chars with mixed case, numbers, symbols
• Enterprise: 14+ chars with no common patterns

⚡ QUICK CHECKLIST
✅ At least 12 characters
✅ Mixed case letters
✅ Numbers and symbols
✅ No personal information
✅ No common patterns
✅ Unique for each account
✅ Two-factor authentication enabled
✅ Using a password manager

Remember: A strong password is your first line of defense!
        """
        
        tips_text.insert(tk.END, tips_content)
        tips_text.config(state=tk.DISABLED)
    
    def create_batch_tab(self, notebook):
        """Create batch analysis tab"""
        batch_frame = ttk.Frame(notebook)
        notebook.add(batch_frame, text="📊 Batch Analysis")
        
        # Input section
        input_frame = ttk.LabelFrame(batch_frame, text="Password List Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter passwords (one per line):", style='Heading.TLabel').pack(anchor=tk.W)
        
        self.batch_input_text = scrolledtext.ScrolledText(input_frame, height=8, font=('Arial', 10))
        self.batch_input_text.pack(fill=tk.X, pady=5)
        
        batch_analyze_btn = ttk.Button(input_frame, text="📊 Analyze All", command=self.batch_analyze)
        batch_analyze_btn.pack(pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(batch_frame, text="Batch Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.batch_results_text = scrolledtext.ScrolledText(results_frame, font=('Consolas', 10),
                                                           bg='#34495e', fg='#ecf0f1', insertbackground='#ecf0f1')
        self.batch_results_text.pack(fill=tk.BOTH, expand=True)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
    
    def on_password_change(self, *args):
        """Real-time password strength update"""
        password = self.password_var.get()
        if not password:
            self.strength_var.set("Enter a password")
            self.progress_var.set(0)
            return
        
        # Quick analysis for real-time feedback
        score = self.quick_score(password)
        self.progress_var.set(score)
        
        if score >= 8:
            self.strength_var.set("🏆 Exceptional")
        elif score >= 6:
            self.strength_var.set("🛡️ Very Strong")
        elif score >= 4:
            self.strength_var.set("💪 Strong")
        elif score >= 2:
            self.strength_var.set("👍 Moderate")
        else:
            self.strength_var.set("⚠️ Weak")
    
    def quick_score(self, password):
        """Quick scoring for real-time feedback"""
        if not password:
            return 0
        
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            score += 1
        
        # Entropy bonus
        entropy = self.calculate_entropy(password)
        if entropy >= 60:
            score += 1
        if entropy >= 80:
            score += 1
        
        # Pattern penalty
        if re.search(r'(.)\1{2,}', password):
            score -= 1
        
        return max(0, min(10, score))
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        if not password:
            return 0.0
        
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            charset_size += len(self.special_chars)
        
        if charset_size == 0:
            return 0.0
        
        return len(password) * math.log2(charset_size)
    
    def analyze_password_gui(self):
        """Perform comprehensive password analysis for GUI"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to analyze.")
            return
        
        # Show loading message
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔍 Analyzing password... Please wait...\n")
        self.root.update()
        
        # Perform analysis in a separate thread to prevent GUI freezing
        threading.Thread(target=self._analyze_password_thread, args=(password,), daemon=True).start()
    
    def _analyze_password_thread(self, password):
        """Analyze password in a separate thread"""
        analysis = self.analyze_password_comprehensive(password)
        
        # Update GUI in main thread
        self.root.after(0, self._update_analysis_results, analysis)
    
    def _update_analysis_results(self, analysis):
        """Update analysis results in GUI"""
        self.results_text.delete(1.0, tk.END)
        
        if "error" in analysis:
            self.results_text.insert(tk.END, f"❌ Error: {analysis['error']}\n")
            return
        
        # Format results
        results = f"""
🔐 PASSWORD ANALYSIS RESULTS
{'=' * 50}

🎯 BASIC METRICS
Password Length: {analysis['length']} characters
Strength Rating: {analysis['strength']} {analysis['emoji']}
Security Score: {analysis['score']}/10
Entropy: {analysis['entropy']:.1f} bits
Estimated Crack Time: {analysis['crack_time']}

🔍 BREACH CHECK
{'🚨 WARNING: Found in data breaches!' if analysis['is_breached'] else '✅ Not found in known breaches'}

📊 CHARACTER ANALYSIS
Uppercase letters: {'✅' if analysis['has_upper'] else '❌'}
Lowercase letters: {'✅' if analysis['has_lower'] else '❌'}
Numbers: {'✅' if analysis['has_digit'] else '❌'}
Special characters: {'✅' if analysis['has_special'] else '❌'}
"""

        if analysis['patterns']:
            results += "\n⚠️ SECURITY ISSUES DETECTED\n"
            for pattern in analysis['patterns']:
                results += f"• {pattern}\n"

        results += "\n🏛️ COMPLIANCE STANDARDS\n"
        for standard, passes in analysis['compliance'].items():
            status = "✅" if passes else "❌"
            results += f"{standard.replace('_', ' ')}: {status}\n"

        results += "\n💡 RECOMMENDATIONS\n"
        if analysis['score'] < 7:
            if analysis['length'] < 12:
                results += "• Increase length to at least 12 characters\n"
            if not analysis['has_upper']:
                results += "• Add uppercase letters\n"
            if not analysis['has_lower']:
                results += "• Add lowercase letters\n"
            if not analysis['has_digit']:
                results += "• Add numbers\n"
            if not analysis['has_special']:
                results += "• Add special characters\n"
            if analysis['patterns']:
                results += "• Avoid predictable patterns\n"
            if analysis['is_breached']:
                results += "• Use a completely different password\n"
        else:
            results += "• Excellent password! Consider using a password manager\n"
            results += "• Enable two-factor authentication where possible\n"

        self.results_text.insert(tk.END, results)
    
    def analyze_password_comprehensive(self, password):
        """Comprehensive password analysis"""
        if not password:
            return {"error": "Password cannot be empty"}
        
        # Basic metrics
        length = len(password)
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(f'[{re.escape(self.special_chars)}]', password))
        
        # Advanced analysis
        entropy = self.calculate_entropy(password)
        patterns = self.check_patterns(password)
        compliance = self.check_compliance(password)
        crack_time = self.estimate_crack_time(password)
        
        # Simulate breach check
        time.sleep(0.1)  # Simulate API delay
        is_breached = self.simulate_breach_check(password)
        
        # Calculate score
        score = self.calculate_comprehensive_score(password, has_upper, has_lower, 
                                                 has_digit, has_special, entropy, 
                                                 patterns, is_breached)
        
        # Determine strength
        strength, emoji = self.determine_strength(score)
        
        return {
            "password": password,
            "length": length,
            "has_upper": has_upper,
            "has_lower": has_lower,
            "has_digit": has_digit,
            "has_special": has_special,
            "entropy": entropy,
            "patterns": patterns,
            "compliance": compliance,
            "crack_time": crack_time,
            "is_breached": is_breached,
            "score": score,
            "strength": strength,
            "emoji": emoji
        }
    
    def check_patterns(self, password):
        """Check for weak patterns"""
        issues = []
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            issues.append("Contains repeated characters")
        
        # Check for sequential patterns
        for pattern in self.common_passwords['patterns']:
            if re.search(pattern, password.lower()):
                issues.append("Contains sequential or keyboard patterns")
                break
        
        # Check for common words
        password_lower = password.lower()
        for word in self.common_passwords['english']:
            if word in password_lower:
                issues.append(f"Contains common word: '{word}'")
        
        # Check for date patterns
        if re.search(r'(19|20)\d{2}', password):
            issues.append("Contains year pattern")
        
        return issues
    
    def check_compliance(self, password):
        """Check compliance with security standards"""
        compliance = {
            'NIST_Basic': len(password) >= 8,
            'NIST_Recommended': len(password) >= 12,
            'PCI_DSS': (len(password) >= 8 and 
                       re.search(r'[A-Z]', password) and 
                       re.search(r'[a-z]', password) and 
                       re.search(r'[0-9]', password) and 
                       re.search(f'[{re.escape(self.special_chars)}]', password)),
            'Enterprise_Grade': (len(password) >= 14 and 
                               re.search(r'[A-Z]', password) and 
                               re.search(r'[a-z]', password) and 
                               re.search(r'[0-9]', password) and 
                               re.search(f'[{re.escape(self.special_chars)}]', password) and
                               len(self.check_patterns(password)) == 0)
        }
        return compliance
    
    def estimate_crack_time(self, password):
        """Estimate time to crack password"""
        entropy = self.calculate_entropy(password)
        guesses_per_second = 1e9
        possible_combinations = 2 ** (entropy - 1)
        seconds_to_crack = possible_combinations / guesses_per_second
        
        if seconds_to_crack < 1:
            return "Less than 1 second"
        elif seconds_to_crack < 60:
            return f"{seconds_to_crack:.1f} seconds"
        elif seconds_to_crack < 3600:
            return f"{seconds_to_crack/60:.1f} minutes"
        elif seconds_to_crack < 86400:
            return f"{seconds_to_crack/3600:.1f} hours"
        elif seconds_to_crack < 31536000:
            return f"{seconds_to_crack/86400:.1f} days"
        elif seconds_to_crack < 31536000000:
            return f"{seconds_to_crack/31536000:.1f} years"
        else:
            return "Centuries to millennia"
    
    def simulate_breach_check(self, password):
        """Simulate breach database check"""
        weak_indicators = ['123', 'password', 'admin', 'qwerty']
        return any(indicator in password.lower() for indicator in weak_indicators)
    
    def calculate_comprehensive_score(self, password, has_upper, has_lower, 
                                    has_digit, has_special, entropy, patterns, is_breached):
        """Calculate comprehensive password score"""
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        
        # Character variety
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 1
        
        # Entropy bonus
        if entropy >= 60:
            score += 1
        if entropy >= 80:
            score += 1
        
        # Pattern penalty
        if len(patterns) == 0:
            score += 1
        
        # Breach penalty
        if is_breached:
            score = max(0, score - 3)
        
        return min(10, score)
    
    def determine_strength(self, score):
        """Determine password strength level"""
        if score >= 9:
            return "Exceptional", "🏆"
        elif score >= 7:
            return "Very Strong", "🛡️"
        elif score >= 5:
            return "Strong", "💪"
        elif score >= 3:
            return "Moderate", "👍"
        elif score >= 1:
            return "Weak", "⚠️"
        else:
            return "Very Weak", "🚨"
    
    def generate_password_gui(self):
        """Generate password with GUI settings"""
        length = self.length_var.get()
        
        chars = ""
        if self.include_lower_var.get():
            chars += string.ascii_lowercase
        if self.include_upper_var.get():
            chars += string.ascii_uppercase
        if self.include_digits_var.get():
            chars += string.digits
        if self.include_symbols_var.get():
            chars += self.special_chars
        
        if not chars:
            messagebox.showwarning("Warning", "Please select at least one character type.")
            return
        
        if length < 8:
            length = 8
            self.length_var.set(8)
            messagebox.showinfo("Info", "Minimum length set to 8 characters.")
        
        # Ensure at least one of each selected type
        password = []
        if self.include_lower_var.get():
            password.append(random.choice(string.ascii_lowercase))
        if self.include_upper_var.get():
            password.append(random.choice(string.ascii_uppercase))
        if self.include_digits_var.get():
            password.append(random.choice(string.digits))
        if self.include_symbols_var.get():
            password.append(random.choice(self.special_chars))
        
        # Fill remaining length
        for _ in range(length - len(password)):
            password.append(random.choice(chars))
        
        # Shuffle
        random.shuffle(password)
        generated = ''.join(password)
        
        self.generated_password_var.set(generated)
    
    def copy_password(self):
        """Copy generated password to clipboard"""
        password = self.generated_password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    
    def analyze_generated(self):
        """Analyze the generated password"""
        password = self.generated_password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No generated password to analyze.")
            return
        
        self.password_var.set(password)
        self.analyze_password_gui()
    
    def generate_multiple_passwords(self):
        """Generate multiple passwords"""
        count = self.multi_count_var.get()
        self.multi_results_text.delete(1.0, tk.END)
        
        self.multi_results_text.insert(tk.END, f"🎲 Generated {count} passwords:\n")
        self.multi_results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for i in range(count):
            self.generate_password_gui()
            password = self.generated_password_var.get()
            score = self.quick_score(password)
            strength, emoji = self.determine_strength(score)
            
            self.multi_results_text.insert(tk.END, f"{i+1:2d}. {password} | {strength} {emoji} ({score}/10)\n")
        
        self.multi_results_text.insert(tk.END, f"\n💡 Copy any password you like and use the 'Analyze' button for detailed analysis.")
    
    def batch_analyze(self):
        """Analyze multiple passwords from batch input"""
        passwords_text = self.batch_input_text.get(1.0, tk.END).strip()
        if not passwords_text:
            messagebox.showwarning("Warning", "Please enter passwords to analyze.")
            return
        
        passwords = [p.strip() for p in passwords_text.split('\n') if p.strip()]
        if not passwords:
            messagebox.showwarning("Warning", "No valid passwords found.")
            return
        
        self.batch_results_text.delete(1.0, tk.END)
        self.batch_results_text.insert(tk.END, f"📊 Batch Analysis of {len(passwords)} passwords\n")
        self.batch_results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        total_score = 0
        for i, password in enumerate(passwords, 1):
            analysis = self.analyze_password_comprehensive(password)
            total_score += analysis['score']
            
            self.batch_results_text.insert(tk.END, 
                f"{i:2d}. {analysis['strength']} {analysis['emoji']} (Score: {analysis['score']}/10) | "
                f"Length: {analysis['length']} | Entropy: {analysis['entropy']:.1f}\n")
            
            if analysis['is_breached']:
                self.batch_results_text.insert(tk.END, "    🚨 Found in breaches!\n")
            
            if analysis['patterns']:
                self.batch_results_text.insert(tk.END, f"    ⚠️ Issues: {len(analysis['patterns'])}\n")
        
        avg_score = total_score / len(passwords)
        self.batch_results_text.insert(tk.END, f"\n📈 SUMMARY\n")
        self.batch_results_text.insert(tk.END, f"Average Security Score: {avg_score:.1f}/10\n")
        
        if avg_score >= 7:
            self.batch_results_text.insert(tk.END, "🎉 Excellent overall password security!\n")
        elif avg_score >= 5:
            self.batch_results_text.insert(tk.END, "👍 Good security, but room for improvement\n")
        else:
            self.batch_results_text.insert(tk.END, "⚠️ Consider strengthening your passwords\n")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = PasswordCheckerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
