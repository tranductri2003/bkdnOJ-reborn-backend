# Generated by Django 4.0.4 on 2022-06-24 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compete', '0004_alter_contest_frozen_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='format_name',
            field=models.CharField(choices=[('default', 'Default'), ('icpc', 'ICPC'), ('ioi', 'IOI')], default='icpc', help_text='The contest format module to use.', max_length=32, verbose_name='contest format'),
        ),
    ]
