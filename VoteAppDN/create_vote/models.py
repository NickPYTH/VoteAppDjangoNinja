from django.db import models
from django.core import validators


class Form(models.Model):
    uniq_key = models.CharField(max_length=20)
    form_name = models.CharField(
        max_length=300,
        validators=[
            validators.MinLengthValidator(3, message="Слишком короткое имя формы"),
            validators.MaxLengthValidator(500, message="Слишком длинное имя формы"),
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
        ],
        verbose_name="Пароль к результатам",
    )
    form_link = models.CharField(
        max_length=300,
        unique=True,
        verbose_name="Ссылка",
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
        max_length=500,
        validators=[
            validators.MinLengthValidator(
                4, message="Слишком короткий заголвок вопроса"
            ),
            validators.MaxLengthValidator(
                500, message="Слишком длинный заголовок вопроса"
            ),
        ],
        verbose_name="Заголовок вопроса",
    )
    question_description = models.CharField(
        max_length=500,
        validators=[
            validators.MaxLengthValidator(
                500, message="Слишком длинное описание вопроса"
            ),
        ],
        verbose_name="Описание вопроса",
    )
    question_comment = models.BooleanField(verbose_name="Наличие комментария", default=False)

    def __str__(self):
        return "{0} | {1}".format(self.form.form_name, self.question_name)

class Answer(models.Model):
    uniq_key = models.CharField(max_length=20)
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        verbose_name="Вопрос")
    answer = models.CharField(
        max_length=500,
        verbose_name="Ответ")
    group = models.CharField(
        max_length=500,
        verbose_name="Группа",
        blank=True,
        null=True)

class SendedForm(models.Model):
    form_key = models.CharField(max_length=50, verbose_name="Ключ формы")
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    answer = models.CharField(max_length=500, verbose_name="Ответ")
    date = models.DateTimeField(auto_now_add=True, editable=False)

class SendedComments(models.Model):
    form_key = models.CharField(max_length=50, verbose_name="Ключ формы")
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    comment = models.CharField(max_length=1000, verbose_name="Комментарий")
    date = models.DateTimeField(auto_now_add=True, editable=False)