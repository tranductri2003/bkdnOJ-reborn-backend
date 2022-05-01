# Generated by Django 4.0.3 on 2022-05-01 10:02

from django.db import migrations, models
import helpers.problem_data
import problem.models.problem_test_data


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_problemtestprofile_testcase_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemtestprofile',
            name='zipfile',
            field=models.FileField(blank=True, null=True, storage=helpers.problem_data.ProblemDataStorage(), upload_to=problem.models.problem_test_data.problem_directory_file),
        ),
    ]
