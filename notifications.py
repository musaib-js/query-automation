from flask_mail import Mail, Message

mail = None 

def init_mail(app):
    """Initialize Flask-Mail with the given app configuration to initialise creds and all."""
    global mail
    mail = Mail(app)

def send_email(to, subject, body):
    """Function to send an email using Flask-Mail."""
    try:
        if not mail:
            raise ValueError("Mail instance is not initialized. Call init_mail(app) first.")
        
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
