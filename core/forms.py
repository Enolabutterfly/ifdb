from .models import User

import django_registration.forms
from captcha.fields import ReCaptchaField


class RegistrationForm(django_registration.forms.RegistrationForm):
    class Meta:
        model = User
        fields = ['email', 'username']

    captcha = ReCaptchaField(label='А вы не робот?')