# Generated by Django 3.2.5 on 2021-07-19 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_vote', '0017_sendedform_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendedComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_key', models.CharField(max_length=50, verbose_name='Ключ формы')),
                ('question', models.CharField(max_length=50, verbose_name='Вопрос')),
                ('comment', models.CharField(max_length=50, verbose_name='Комментарий')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
