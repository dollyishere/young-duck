from django import forms
from .models import Book, Card

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'semi_title', 'cover_image']


class CardForm(forms.ModelForm):
    my_score = forms.FloatField(
        required=False,
        label='평점을 매겨주세요. (최소 0.0, 최대 5.0)',
        widget=forms.NumberInput(
            attrs={
                'step' : 0.5,
                'min' : 0,
                'max' : 5,
            }
        ),
    )
    my_comment = forms.CharField(
        required=False,
        label='감상을 적어주세요.',
        widget=forms.Textarea()
    )
    visited_count = forms.IntegerField(
        required=False,
        label='관람 횟수를 입력해주세요. (관람하지 않았을 시 x)',
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