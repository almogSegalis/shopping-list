from django.db import models

class Item(models.Model):
    item = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    # add author

    def __str__(self):
        return self.item

# Create your models here.
