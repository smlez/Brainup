from django import forms
from brainup_core.models import Card, CardsCollection


class CardCreationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'front_side',
            'back_side',
            'collection'
        ]


class CollectionCreationForm(forms.ModelForm):
    class Meta:
        model = CardsCollection
        fields = [
            'title',
            'description'
        ]

#TODO
# class CardsFilter(forms.ModelForm):
#     class Meta:
#         model = Card
#         fields = [
#             'front_side',
#
#         ]