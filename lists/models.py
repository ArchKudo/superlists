from django.db import models

# Create your models here.

# In Python classes are defined not declared
# Hence classes cannot be forward refrenced


class List(models.Model):
    '''A model for TO-DO lists
    A group of items can belong to a unique list thus,
    Allows creation for multiple lists'''
    pass


class Item(models.Model):
    '''A model for TO-DO list items'''
    text = models.TextField(default='')
    lst = models.ForeignKey(List, default=None)
