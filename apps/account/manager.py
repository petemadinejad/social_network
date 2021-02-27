from django.db import models


class UserManager(models.Manager):
    def check_username_password(self):
        pass
