# Generated by Django 3.2.9 on 2021-11-02 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_vote', '0019_auto_20211101_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FormTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('is_inf', models.BooleanField(null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupsTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('answers', models.ManyToManyField(to='create_vote.AnswersTable')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('serial_number', models.IntegerField()),
                ('is_comment', models.BooleanField(null=True)),
                ('range', models.IntegerField(blank=True, null=True)),
                ('answers', models.ManyToManyField(to='create_vote.AnswersTable')),
                ('groups', models.ManyToManyField(to='create_vote.GroupsTable')),
            ],
        ),
        migrations.CreateModel(
            name='TypesTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='form',
        ),
        migrations.DeleteModel(
            name='SendedComments',
        ),
        migrations.DeleteModel(
            name='SendedForm',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Form',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='questiontable',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='create_vote.typestable'),
        ),
        migrations.AddField(
            model_name='formtable',
            name='questions',
            field=models.ManyToManyField(to='create_vote.QuestionTable'),
        ),
    ]
