from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return 'Message From '+ self.name + ' - ' + self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile of '+ self.user.email
