# Generated by Django 4.2.4 on 2023-09-14 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="message_type",
            field=models.CharField(
                choices=[
                    ("SYSTEM", "System Message"),
                    ("USER", "User Message"),
                    ("CONTEXT", "VectorDB Context"),
                    ("LLM", "LLM Message"),
                ],
                max_length=10,
            ),
        ),
    ]
