from django.contrib import admin

# Register your models here.

from .models import Ques, Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
admin.site.register(Ques, QuestionAdmin)
admin.site.register(Choice)