from django.db import models

class History(models.Model):
    token = models.TextField()
    chat_id = models.TextField()
    message = models.TextField()