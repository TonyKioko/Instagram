from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives

def send_activation_email(user, current_site, receiver):
    subject = 'Activate your pixagram account'
    sender = 'tonnibravo12@gmail.com'
    message = render_to_string('registration/acc_active_email.html', {
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    msg = EmailMultiAlternatives(subject,message,sender,[receiver])
    # msg.attach_alternative(html_content,'text/html')
    # msg = EmailMessage(subject, message, to=[receiver])
    # msg.send()
    # send_mail(msg)
