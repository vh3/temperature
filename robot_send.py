# email function for the data robot.
# 
# 17 Nov 2019, vh, split the email functions from the sensor reading functions

# Send a file by email!
# After: https://realpython.com/python-send-email/
def send_email(email_destination,filename,timestamp):

    import email, smtplib, ssl

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    subject        = "Temperature sensor experiment " + timestamp
    body           = "Temperature sensor experiment data sent to you by your friendly neighbourhood data robot."
    sender_email   = "<sender email address here"
    sender_display_name = "<sender display name here> <sender email address here>"
    password       = "<password here>"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"]    = sender_display_name
    message["To"]      = email_destination
    message["Subject"] = subject
    # message["Bcc"]     = email_destination  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open our attachment file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_display_name, email_destination, text)

    return
