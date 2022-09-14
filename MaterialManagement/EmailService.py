import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def SendMail(receiver_email, message):
 smtp_server = "smtp.gmail.com"
 port = 587  # For starttls
 sender_email = "advaninikhil19@gmail.com"
 password = "NIKHILadvani2001"

# Create a secure SSL context
 context = ssl.create_default_context()

# Try to log in to server and send email
 try:
    server = smtplib.SMTP(smtp_server, port)

    server.starttls(context=context)  # Secure the connection

    server.login(sender_email, password)
    # TODO: Send email here
    server.sendmail(sender_email, receiver_email, message)
 except Exception as e:
    # Print any error messages to stdout
    print(e)
 finally:
    server.quit()
def SendHTMLMail(receiver_email, msg):
    sender_email = "advaninikhil19@gmail.com"
    password = "NIKHILadvani2001"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Employee Password"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = msg
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.sandeepsappal.in">Sandeep Sappal</a> 
           Please Change Your Password
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )