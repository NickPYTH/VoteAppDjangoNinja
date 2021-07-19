from django.contrib import admin
from .models import Form, Question, Answer, SendedForm, SendedComments

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("form_name", "form_password", "form_end_date", "form_created_date")
    list_filter  = ("form_name", "form_password", "form_end_date", "form_created_date")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_type", "question_name", "question_description")
    list_filter  = ("question_type", "question_name", "question_description")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "group", "answer",)
    list_filter  = ("question", "answer", "group",)

@admin.register(SendedForm)
class SendedFormAdmin(admin.ModelAdmin):
    list_display = ("form_key", "question", "answer", "date")
    list_filter  = ("form_key", "question", "answer",)

@admin.register(SendedComments)
class SendedCommentsAdmin(admin.ModelAdmin):
    list_display = ("form_key", "question", "comment", "date")
    list_filter  = ("form_key", "question", "comment",)