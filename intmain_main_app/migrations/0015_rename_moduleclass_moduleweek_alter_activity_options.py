# Generated by Django 4.1.4 on 2023-01-28 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intmain_main_app", "0014_alter_activity_status_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="moduleClass",
            new_name="ModuleWeek",
        ),
        migrations.AlterModelOptions(
            name="activity",
            options={"verbose_name": "05. Notes", "verbose_name_plural": "05. Notes"},
        ),
    ]