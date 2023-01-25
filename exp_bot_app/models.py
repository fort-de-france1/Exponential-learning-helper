from django.db import models


# Create your models here.
class Profile(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Remind(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    date_create = models.DateField(auto_now_add=True)
    date_remind = models.DateField(blank=True, null=True)
    day_repeat = models.IntegerField(blank=True, null=True, default=1)


    def __str__(self):
        return self.title


class CurrentRemind(models.Model):
    telegram = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
    rem = models.ForeignKey(Remind, blank=True, null=True, on_delete=models.SET_NULL)


