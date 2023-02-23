from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50) # bootstrap color
    
    def __str__(self):
        return self.name


class ItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

