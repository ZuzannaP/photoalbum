from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Photo, Comment


admin.site.register(Photo),
admin.site.register(Comment),
