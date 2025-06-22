import re
def check_strength(password):
    score = 0
    feedback = []

    # Criteria checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make your password at least 8 characters long.")

    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one digit (0–9).")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters like !, @, #, etc.")

    # Strength rating
    if score == 4:
        strength = "Strong 💪"
    elif score == 3:
        strength = "Moderate 👍"
    else:
        strength = "Weak ⚠️"

    return strength, feedback

# Main interaction
if __name__ == "__main__":
    print("🔐 Password Strength Checker")
    user_password = input("Enter a password to check: ")

    strength, suggestions = check_strength(user_password)
    print(f"\nYour password is: {strength}")

    if suggestions:
        print("\nSuggestions to improve:")
        for s in suggestions:
            print(f" - {s}")
    ## By Muawiya-contact
    ## GitHub: https://github.com/Muawiya-contact