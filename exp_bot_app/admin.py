from django.contrib import admin

# Register your models here.
from .models import Remind, Profile, CurrentRemind


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "telegram_id", "name"]


@admin.register(Remind)
class RemindAdmin(admin.ModelAdmin):
    list_display = ["profile", "title", "content", "date_create", "date_remind", "day_repeat"]


@admin.register(CurrentRemind)
class CurrentRemindAdmin(admin.ModelAdmin):
    list_display = ["id", "telegram_id", "rem_id"]
