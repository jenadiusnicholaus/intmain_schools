# Generated by Django 4.1.4 on 2023-01-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intmain_main_app", "0028_rename_topic_id_activity_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="modulecategory",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]