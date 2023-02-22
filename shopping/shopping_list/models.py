from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50) # bootstrap color
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name