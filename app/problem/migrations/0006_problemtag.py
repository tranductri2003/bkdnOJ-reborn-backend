# Generated by Django 4.0.4 on 2023-06-05 16:05

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_alter_problemtestprofile_checker_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(db_index=True, help_text="Name of this Problem Tag. Eg: 'dp', 'math', 'binary-search',...", max_length=128, unique=True)),
                ('descriptions', models.TextField(blank=True, default='', help_text='Description of tag')),
                ('tagged_problems', models.ManyToManyField(blank=True, default=[], help_text='Problems those carry this tag', related_name='tags', to='problem.problem')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
