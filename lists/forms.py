from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "Cannot add duplicate items!"


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

    def save(self, lst):
        self.instance.lst = lst
        return super().save()


class ExistingListItemForm(ItemForm):

    def __init__(self, lst, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.lst = lst

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)
