from django import forms
from .models import Book, Card

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'semi_title', 'cover_image']


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ['my_score', 'my_comment', 'visits_count']