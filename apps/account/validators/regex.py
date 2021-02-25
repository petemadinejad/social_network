from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?98?\d{9,15}$')
email_regex = RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
