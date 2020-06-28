from django.contrib import admin
from . models import Post,BlogComment,Bookmark

admin.site.register((Post,BlogComment,Bookmark))
