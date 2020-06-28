from django.db import models
from django.contrib.auth.models import User 
from django.utils.timezone import now 

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=20)
    slug = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return 'comment by: ' + self.user.username
    
class Bookmark(models.Model):
    booksno = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'bookmark by: ' + self.user.username


