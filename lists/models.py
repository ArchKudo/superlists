from django.db import models

# Create your models here.

# In Python classes are defined not declared
# Hence classes cannot be forward refrenced


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    lst = models.ForeignKey(List, default=None)
