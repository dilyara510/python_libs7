# Generated by Django 4.2.7 on 2023-12-05 21:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0006_message_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="file",
            new_name="attachment",
        ),
    ]
