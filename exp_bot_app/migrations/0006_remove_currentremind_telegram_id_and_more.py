# Generated by Django 4.1.5 on 2023-01-19 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exp_bot_app', '0005_currentremind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentremind',
            name='telegram_id',
        ),
        migrations.AddField(
            model_name='currentremind',
            name='telegram',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='exp_bot_app.profile'),
        ),
    ]
