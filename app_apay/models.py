from django.db import models
from django.contrib.auth.models import User

class usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psw = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username}'