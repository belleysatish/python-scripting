import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def send_email(to_email, account_type, old_password, new_password):
    """
    Sends an email with the account details and the new password.
    
    Parameters:
    - to_email (str): Recipient's email address.
    - account_type (str): The type of account.
    - old_password (str): The previous password.
    - new_password (str): The newly generated password.
    """
    # Email configuration
    from_email = "your_email@example.com"  # Replace with your email
    from_password = "your_email_password"  # Replace with your email password
    subject = "Your New Password"

    # Email content
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    body = f"""
    Hello,

    Here are the details for your account:

    - Account Type: {account_type}
    - Old Password: {old_password}
    - New Password: {new_password}

    Please keep your password secure.

    Regards,
    Password Generator
    """
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    account_type = input("Enter the account type (noninteractive/other): ")
    old_password = input("Enter the old password: ")
    user_email = input("Enter the email of the user: ")

    # Generate the password
    new_password = generate_password(account_type, old_password)
    print("Generated Password:", new_password)

    # Send the password via email
    send_email(user_email, account_type, old_password, new_password)
