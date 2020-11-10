from django.contrib import admin
from . models import Contact,Profile

admin.site.register((Contact,Profile))