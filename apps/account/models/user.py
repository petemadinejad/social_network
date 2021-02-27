from django.db import models

# from apps.account.manager import UserManager
from apps.account.validators.regex import email_regex


class User(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=100, verbose_name='Last Name')
    email = models.EmailField(validators=[email_regex], max_length=100, verbose_name='Email', unique=True)
    password = models.CharField(max_length=50, verbose_name='Password')
    repeat_password = models.CharField(max_length=50, verbose_name='Repeat Password')
    is_staff = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        ordering = ('-date_joined',)

    # object = UserManager()
