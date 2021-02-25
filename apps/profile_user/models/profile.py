from django.db import models

from apps.account.models.user import User
from apps.account.validators.regex import phone_regex


class Profile(models.Model):
    ROLE_CHOICES = (
        ('consumer', 'Consumer'),
        ('staff', 'Staff'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('Female', 'Female'),
        ('O', 'other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, default='no bio')
    website_url = models.CharField(blank=True, null=True, max_length=100)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Phone number')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=7, verbose_name='Gender')
    birthday = models.DateField(verbose_name='Birthday', blank=True, null=True)
    profile_pic = models.ImageField('profile_user', blank=True, null=True)
    user_follow = models.ManyToManyField(User, symmetrical=False, related_name='followers', blank=True)
    user_request = models.ManyToManyField(User, symmetrical=False, related_name='requests', blank=True)

    def __str__(self):
        return str(self.user.email)
