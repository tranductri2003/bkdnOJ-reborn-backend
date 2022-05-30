# Generated by Django 4.0.4 on 2022-05-30 18:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemtestprofile',
            name='output_limit',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1073741824)], verbose_name='output limit length'),
        ),
        migrations.AlterField(
            model_name='problemtestprofile',
            name='output_prefix',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1073741824)], verbose_name='output prefix length'),
        ),
    ]