# Generated by Django 3.2.9 on 2021-11-12 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_vote', '0029_sendformcommentstable_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendformtable',
            name='data',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
