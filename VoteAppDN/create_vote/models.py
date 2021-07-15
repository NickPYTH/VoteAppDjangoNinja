from django.db import models
from django.core import validators


class QuestionType(models.Model):
    question_type = models.CharField(max_length=20, verbose_name="Наименование вопроса")

class Form(models.Model):
    form_name = models.CharField(
        max_length=300,
        validators=[
            validators.MinLengthValidator(3, message="Слишком короткое имя формы"),
            validators.MaxLengthValidator(300, message="Слишком длинное имя формы"),
        ],
        unique=True,
        verbose_name="Название формы",
    )
    form_password = models.CharField(
        max_length=20,
        validators=[
            validators.MinLengthValidator(
                4, message="Слишком короткий пароль к результатам"
            ),
            validators.MaxLengthValidator(
                20, message="Слишком длинный пароль к результатам"
            ),
        ],
        verbose_name="Пароль к результатам",
    )
    form_end_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата окончания жизни формы"
    )
    form_created_date = models.DateTimeField(
        verbose_name="Дата создания формы", auto_now_add=True
    )

class Question(models.Model):
    uniq_key = models.CharField(max_length=20)
    question_type = models.CharField(verbose_name="Тип вопроса", max_length=20)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question_name = models.CharField(
        max_length=40,
        validators=[
            validators.MinLengthValidator(
                4, message="Слишком короткий заголвок вопроса"
            ),
            validators.MaxLengthValidator(
                40, message="Слишком длинный заголовок вопроса"
            ),
        ],
        verbose_name="Заголовок вопроса",
    )
    question_description = models.CharField(
        max_length=100,
        validators=[
            validators.MaxLengthValidator(
                100, message="Слишком длинное описание вопроса"
            ),
        ],
        verbose_name="Описание вопроса",
    )
    question_comment = models.BooleanField(verbose_name="Наличие комментария", default=False)

class SubAnswer(models.Model):
    uniq_key = models.CharField(max_length=20)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(
        max_length=30,
        verbose_name="Связанный ответ",)

class Answer(models.Model):
    uniq_key = models.CharField(max_length=20)
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        verbose_name="Вопрос")
    answer = models.CharField(
        max_length=40,
        verbose_name="Ответ")
    sub_answer = models.ManyToManyField(
        SubAnswer, 
        verbose_name="Связанные ответы",
        null=True,
        blank=True)