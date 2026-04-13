from django import forms
from .models import Item, UserProfile


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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
            'image',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-styling'
