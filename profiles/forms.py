from django import forms
from .models import Item


class WishForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = (
            'name',
            'done',
            'image',
            'link',
            'description',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-styling'