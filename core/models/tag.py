from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name