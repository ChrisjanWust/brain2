# Generated by Django 4.1.9 on 2023-06-02 23:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0003_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="body",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
