from django import forms
from .models import Book, Card

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = []


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        exclude = []