# Generated by Django 3.2.5 on 2021-07-12 04:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=300, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Слишком короткое имя формы'), django.core.validators.MaxLengthValidator(300, message='Слишком длинное имя формы')], verbose_name='Название формы')),
                ('form_password', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(4, message='Слишком короткий пароль к результатам'), django.core.validators.MaxLengthValidator(20, message='Слишком длинный пароль к результатам')], verbose_name='Пароль к результатам')),
                ('form_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания жизни формы')),
                ('form_created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания формы')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=20, verbose_name='Наименование вопроса')),
            ],
        ),
        migrations.CreateModel(
            name='SubAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30, verbose_name='Связанный ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(4, message='Слишком короткий заголвок вопроса'), django.core.validators.MaxLengthValidator(40, message='Слишком длинный заголовок вопроса')], verbose_name='Заголовок вопроса')),
                ('question_description', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator(100, message='Слишком длинное описание вопроса')], verbose_name='Описание вопроса')),
                ('question_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_vote.form')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=40, verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_vote.question', verbose_name='Вопрос')),
                ('sub_answer', models.ManyToManyField(blank=True, null=True, to='create_vote.SubAnswer', verbose_name='Связанные ответы')),
            ],
        ),
    ]