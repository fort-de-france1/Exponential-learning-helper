# Generated by Django 4.1.5 on 2023-01-23 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exp_bot_app', '0013_alter_remind_day_repeat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remind',
            name='day_repeat',
        ),
    ]
