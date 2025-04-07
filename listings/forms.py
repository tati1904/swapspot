from django import forms
from .models import Item
from .models import Message
from .models import Review

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'condition', 'image']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']



