from django.contrib import admin
from .models import *


@admin.register(FormTable)
class FormAdmin(admin.ModelAdmin):
    pass
    #  list_display = ("form_name", "form_password", "form_end_date", "form_created_date")
    #  list_filter = ("form_name", "form_password", "form_end_date", "form_created_date")


@admin.register(QuestionTable)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TypesTable)
class TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswersTable)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupsTable)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(SendFormTable)
class SendFormAdmin(admin.ModelAdmin):
    pass


@admin.register(SendFormCommentsTable)
class SendFormCommentsAdmin(admin.ModelAdmin):
    pass


