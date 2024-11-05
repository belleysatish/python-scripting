import random
import string

def generate_password(account_type, old_password):
    """
    Generate a secure password based on account type and an existing password for comparison.
    
    Parameters:
    - account_type (str): The type of account ('noninteractive' or 'other').
    - old_password (str): The previous password to ensure a minimum difference.
    
    Returns:
    - str: A newly generated password that meets security criteria.
    """
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    symbols = '_$#'

    # Set requirements based on account type
    if account_type == 'noninteractive':
        min_length = 20
        min_diff = 10
    elif account_type == 'other':
        min_length = 16
        min_diff = 4
    else:
        raise ValueError("Invalid account type. Choose 'noninteractive' or 'other'.")

    # Ensure at least 2 lowercase, 2 uppercase, 2 digits, and 2 symbols in the password
    password = (
        ''.join(random.choice(lowercase_letters) for _ in range(2)) +
        ''.join(random.choice(uppercase_letters) for _ in range(2)) +
        ''.join(random.choice(digits) for _ in range(2)) +
        ''.join(random.choice(symbols) for _ in range(2))
    )

    # Generate additional random characters to meet the minimum length
    while len(password) < min_length:
        password += random.choice(string.ascii_letters + string.digits + symbols)

    # Ensure the password has the required minimum difference from the old password
    diff_count = sum(c1 != c2 for c1, c2 in zip(password, old_password))
    while diff_count < min_diff or len(password) < min_length:
        # Replace part of the password with new random characters
        password = (
            password[:2] + ''.join(random.choice(string.ascii_letters + string.digits + symbols) 
                                   for _ in range(len(password) - 2))
        )
        # Recalculate the difference count
        diff_count = sum(c1 != c2 for c1, c2 in zip(password, old_password))

    return password

# Example usage
if __name__ == "__main__":
    account_type = input("Enter the account type (noninteractive/other): ")
    old_password = input("Enter the old password: ")
    
    new_password = generate_password(account_type, old_password)
    print("Generated Password:", new_password)
