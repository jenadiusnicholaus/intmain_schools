# Generated by Django 4.1.4 on 2023-01-28 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("intmain_main_app", "0023_alter_module_options_alter_weeks_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weeks",
            name="module",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="module_week",
                to="intmain_main_app.module",
            ),
        ),
    ]
