# Generated by Django 4.1.4 on 2023-01-28 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("intmain_main_app", "0016_alter_weeks_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="activity",
            options={
                "verbose_name": "05. Activity",
                "verbose_name_plural": "05. Activity",
            },
        ),
        migrations.AlterModelOptions(
            name="moduleweek",
            options={
                "ordering": ("Weeks", "module"),
                "verbose_name": "02_2. module Week",
                "verbose_name_plural": "02_2. module Week",
            },
        ),
        migrations.CreateModel(
            name="ModuleEnrolemnet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enrollement_status",
                    models.CharField(
                        choices=[
                            ("full_enrolled", "Full enrolled"),
                            ("partial_enrolled", "Partial enrolled"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "modules",
                    models.ManyToManyField(
                        related_name="enroled_module_set", to="intmain_main_app.module"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="enroled_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "ModuleEnrolemnet",
                "verbose_name_plural": "ModuleEnrolemnets",
            },
        ),
    ]
