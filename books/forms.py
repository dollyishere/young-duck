from django import forms
from .models import Book, Card

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'semi_title', 'cover_image']


class CardForm(forms.ModelForm):
    my_score = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'step' : 0.5,
                'min' : 0,
                'max' : 5,
            }
        ),
    )
    my_comment = forms.CharField(
        widget=forms.Textarea()
    )
    visited_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'step' : 1,
                'min' : 0,
            }
        ),
    )

    class Meta:
        model = Card
        fields = ['my_score', 'my_comment', 'visited_count']