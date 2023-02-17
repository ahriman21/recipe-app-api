from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from .tag import Tag
import os
import uuid

#models
def recipe_image_path(instance,filename):
    ext = filename.split('.')[1]
    name = f'{uuid.uuid4()}.{ext}'
    final = os.path.join('upload','recipe',name)
    return final


class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    price = models.PositiveIntegerField()
    time_minutes = models.PositiveSmallIntegerField()
    link = models.CharField(max_length=255,blank=True,null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(blank=True,null=True,upload_to=recipe_image_path)

    def __str__(self):
        return self.title