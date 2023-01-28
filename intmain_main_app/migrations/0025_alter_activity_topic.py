# Generated by Django 4.1.4 on 2023-01-28 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("intmain_main_app", "0024_alter_weeks_module"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="topic",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="activity_set",
                to="intmain_main_app.topics",
            ),
        ),
    ]
