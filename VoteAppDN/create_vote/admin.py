from django.contrib import admin
from .models import QuestionType, Form, Question, SubAnswer, Answer

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ("question_type",)
    list_filter  = ("question_type",)

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("form_name", "form_password", "form_end_date", "form_created_date")
    list_filter  = ("form_name", "form_password", "form_end_date", "form_created_date")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_type", "question_name", "question_description")
    list_filter  = ("question_type", "question_name", "question_description")

@admin.register(SubAnswer)
class SubAnswerAdmin(admin.ModelAdmin):
    list_display = ("value",)
    list_filter  = ("value",)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "answer",)
    list_filter  = ("question", "answer",)