# Generated by Django 3.2.5 on 2021-07-17 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_vote', '0012_auto_20210717_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='form_link',
            field=models.CharField(default=1, max_length=300, unique=True, verbose_name='Ссылка'),
            preserve_default=False,
        ),
    ]
