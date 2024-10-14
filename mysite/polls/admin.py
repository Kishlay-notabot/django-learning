from django.contrib import admin

# Register your models here.

from .models import Ques, Choice

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
admin.site.register(Ques, QuestionAdmin)
admin.site.register(Choice)