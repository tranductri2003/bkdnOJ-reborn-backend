# Generated by Django 4.0.4 on 2022-06-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_remove_organization_logo_override_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='short_name',
            field=models.CharField(help_text='To identify each org from their sibling orbs. Also is displayed beside user name during contests.', max_length=64, verbose_name='short name'),
        ),
    ]
