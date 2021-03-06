from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

# In Python classes are defined not declared
# Hence classes cannot be forward refrenced


class List(models.Model):
    '''A model for TO-DO lists
    A group of items can belong to a unique list thus,
    Allows creation for multiple lists'''

    def get_absolute_url(self):
        return reverse('list_page', args=[self.id])


class Item(models.Model):
    '''A model for TO-DO list items'''
    text = models.TextField(default='')
    lst = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('lst', 'text')
