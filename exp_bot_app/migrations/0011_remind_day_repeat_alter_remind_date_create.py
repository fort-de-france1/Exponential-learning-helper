# Generated by Django 4.1.5 on 2023-01-23 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exp_bot_app', '0010_alter_remind_date_remind'),
    ]

    operations = [
        migrations.AddField(
            model_name='remind',
            name='day_repeat',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='remind',
            name='date_create',
            field=models.DateField(auto_now_add=True),
        ),
    ]
