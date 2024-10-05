from django.contrib import admin

# Register your models here.

from .models import Ques, Choice

admin.site.register(Ques)
admin.site.register(Choice)