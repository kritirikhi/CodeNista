from django.db import models

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return 'Message From '+ self.name + ' - ' + self.email
