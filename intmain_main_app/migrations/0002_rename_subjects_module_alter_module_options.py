# Generated by Django 4.1.4 on 2023-01-27 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("intmain_main_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Subjects",
            new_name="Module",
        ),
        migrations.AlterModelOptions(
            name="module",
            options={
                "verbose_name": "02. Subject",
                "verbose_name_plural": "02. Module",
            },
        ),
    ]