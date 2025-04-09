from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = 'ActivationEmail.html'

class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'ConfirmationEmail.html'