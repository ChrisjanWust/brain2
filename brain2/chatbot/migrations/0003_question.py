# Generated by Django 4.1.9 on 2023-06-02 23:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot", "0002_keyword"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("query", models.CharField(max_length=200)),
                ("generated_context", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]