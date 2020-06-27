from django.contrib import admin
from . models import Post,BlogComment,Bookmark,Postview

admin.site.register((Post,BlogComment,Bookmark,Postview))
