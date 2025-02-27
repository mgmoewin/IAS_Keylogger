import smtplib
import ssl

def sendEmail(message):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "moewin4070@gmail.com"  # Replace with your sender email
    password = "myru mrlh bjro qhhz"           # Use your Gmail app password
    receiver_email ="htoonaylin022@gmail.com"  # Replace with receiver email

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Identify to the SMTP server
            server.starttls(context=context)  # Encrypt the connection
            server.ehlo()  # Re-identify after encryption
            server.login(sender_email, password)  # Use password instead of receiver_email
            server.sendmail(sender_email, receiver_email, message)  # Send the email
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
