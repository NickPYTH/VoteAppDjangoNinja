# Generated by Django 3.2.9 on 2021-11-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_vote', '0026_auto_20211111_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='formtable',
            name='password',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]