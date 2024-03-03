from comms.mail import send_mail

def send_reset_password_email(user, otp):
    """reset password email"""
    subject = "Grabem Account Password Reset"
    body = f"""
        <html>
        <head></head>
        <body>
            <p>Hello {user.username},</p>
            <p>You have requested to reset your password</p>
            
            <p> Your OTP is {otp}</p>

            <p>This OTP will expire in 30 minutes</p>
            <p>Ignore this message if you did not perform this action.</p>
        </body>
        </html>
        """
    send_mail(user.email, subject, body)

def send_change_email(user, token):
    """reset email"""
    subject = "Grabem Account Email Reset"
    body = f"""
        <html>
        <head></head>
        <body>
            <p>Hello {user.username},</p>
            
            <p>You have requested to change your email</p>

            <p>Your OTP is {token}</p>
            <p>This OTP will expire in 30 minutes</p>
            <p>Ignore this message if you did not perform this action.</p>
        </body>
        </html>
        """
    send_mail(user.email, subject, body)
