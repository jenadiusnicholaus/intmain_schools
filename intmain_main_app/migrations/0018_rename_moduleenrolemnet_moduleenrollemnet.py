# Generated by Django 4.1.4 on 2023-01-28 09:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "intmain_main_app",
            "0017_alter_activity_options_alter_moduleweek_options_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ModuleEnrolemnet",
            new_name="ModuleEnrollemnet",
        ),
    ]
