# Generated by Django 4.1.4 on 2023-01-27 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "intmain_main_app",
            "0008_alter_moduleclass_options_alter_weeks_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="weeks",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]