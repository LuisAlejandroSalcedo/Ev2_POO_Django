from django.db import models

class Reminder(models.Model):
    content = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder: {self.content}. Created at {self.createdAt.timestamp()}. Important: {self.important}"