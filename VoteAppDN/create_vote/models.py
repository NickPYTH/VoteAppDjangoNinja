from django.db import models
from django.core import validators


class TypesTable(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class AnswersTable(models.Model):
    value = models.CharField(max_length=200, blank=True, null=False)

    def __str__(self):
        return self.value


class GroupsTable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    answers = models.ManyToManyField(AnswersTable)

    def __str__(self):
        return self.name


class QuestionTable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    serial_number = models.IntegerField(blank=False, null=False)
    type = models.ForeignKey(TypesTable, on_delete=models.DO_NOTHING)
    is_comment = models.BooleanField(blank=False, null=True, default=False)
    range = models.IntegerField(blank=True, null=True)
    answers = models.ManyToManyField(AnswersTable)
    groups = models.ManyToManyField(GroupsTable)

    def __str__(self):
        return self.name


class FormTable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    password = models.CharField(max_length=200, blank=True, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    is_inf = models.BooleanField(blank=False, null=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    questions = models.ManyToManyField(QuestionTable)
    enter_code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SendAnswerTable(models.Model):
    question = models.ForeignKey(QuestionTable, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(GroupsTable, on_delete=models.DO_NOTHING, blank=True, null=True)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question.name


class SendFormTable(models.Model):
    form = models.ForeignKey(FormTable, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(auto_now=True)
    answers = models.ManyToManyField(SendAnswerTable)

    def __str__(self):
        return self.form.name


class SendFormCommentsTable(models.Model):
    form = models.ForeignKey(SendFormTable, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(QuestionTable, on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value
