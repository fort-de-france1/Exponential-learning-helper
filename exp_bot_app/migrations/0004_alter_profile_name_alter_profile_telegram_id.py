# Generated by Django 4.1.5 on 2023-01-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exp_bot_app', '0003_remind_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telegram_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
