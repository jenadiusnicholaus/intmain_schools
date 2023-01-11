# Generated by Django 4.1.4 on 2023-01-11 19:16

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0008_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True,
                default="intmain_avatar.png",
                upload_to=authentication.models.Profile.image_upload_to,
            ),
        ),
    ]