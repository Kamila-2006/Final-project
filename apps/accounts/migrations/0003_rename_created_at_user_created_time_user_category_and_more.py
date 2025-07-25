# Generated by Django 5.2 on 2025-07-12 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_phone_number"),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="created_at",
            new_name="created_time",
        ),
        migrations.AddField(
            model_name="user",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sellers",
                to="store.category",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="project_name",
            field=models.CharField(default="default-project", max_length=50),
            preserve_default=False,
        ),
    ]
