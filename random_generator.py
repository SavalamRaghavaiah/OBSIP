import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Random Password Generator")
    
    length = int(input("Enter password length: "))
    use_letters = input("Include letters (yes/no)? ").lower() == 'yes'
    use_numbers = input("Include numbers (yes/no)? ").lower() == 'yes'
    use_symbols = input("Include symbols (yes/no)? ").lower() == 'yes'
    
    try:
        password = generate_password(length, use_letters, use_numbers, use_symbols)
        print(f"Generated password: {password}")
    except ValueError as ve:
        print(ve)

if __name__ == "__main__":
    main()