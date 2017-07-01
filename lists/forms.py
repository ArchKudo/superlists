from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        '''Specify which model the form is for,
        which fields of the model should be used'''
        model = Item
        fields = ('text',)
        widgets = {'text': forms.fields.TextInput(
            attrs={'placeholder': 'Enter an item',
                   'class': 'form-control input-lg', }), }

        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
