from django.conf import settings
from django.core.mail import send_mail,BadHeaderError


class MessageHandler:
    email = None
    otp = None

    def __init__(self, email, otp):
        self.email = email
        self.otp = otp

    def send_otp_via_email(self):
        subject = 'OTP Verification'
        message = f'Your OTP is: {self.otp}'

        try:
            # Envoyer l'e-mail avec l'OTP
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )
            print("OTP sent successfully!")
        except BadHeaderError:
            # Gérer spécifiquement l'erreur de mauvais en-tête
            print("Error: Bad header found in the email")
        except Exception as e:
            # Gérer toutes les autres erreurs génériques
            print(f'Error: {e}')
    # def send_otp_via_message(self):     
    #     client= Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    #     message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.phone_number}' )
    # def send_otp_via_whatsapp(self):     
    #     client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
    #     message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')
