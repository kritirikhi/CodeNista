from django.contrib import admin
from . models import Post,BlogComment,Bookmark,PostView

admin.site.register((Post,BlogComment,Bookmark,PostView))
