# Generated by Django 5.0 on 2024-09-10 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0013_user_gain_user_wallet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="people_you_may_know",
        ),
    ]
