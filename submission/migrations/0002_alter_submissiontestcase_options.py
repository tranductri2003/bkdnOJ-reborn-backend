# Generated by Django 4.0.4 on 2022-07-14 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissiontestcase',
            options={'ordering': ['case', 'id'], 'verbose_name': 'submission test case', 'verbose_name_plural': 'submission test cases'},
        ),
    ]
