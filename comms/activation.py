from comms.mail import send_mail
from account.models import OTP

def send_activation_mail(user):
    subject = "Grabem Account Activation"
    user_otp = OTP.objects.create(user=user, purpose='registration')
    body = f"""
        <html>
        <head></head>
        <body>
            <p>Hello There,</p>
            <p>Thank you for registering on our platform.</p>
            
            <p>Your OTP is {user_otp.code}</p>
            <p>This OTP expires in 30 minutes</p>
            <p>Ignore this message if you did not register on our platform.</p>
        </body>
        </html>
        """
    
    send_mail(user.email, subject, body)