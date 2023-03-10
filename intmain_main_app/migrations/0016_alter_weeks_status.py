# Generated by Django 4.1.4 on 2023-01-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "intmain_main_app",
            "0015_rename_moduleclass_moduleweek_alter_activity_options",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="weeks",
            name="status",
            field=models.CharField(
                choices=[
                    ("not_start", "No Started"),
                    ("started", "Started"),
                    ("reviewed", "reviewed"),
                    ("done", "Done"),
                    ("incomplete", "Incomplate"),
                ],
                default="not_start",
                max_length=20,
                null=True,
            ),
        ),
    ]
