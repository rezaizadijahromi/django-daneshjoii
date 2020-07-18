from django import forms

from .models import (
    Question, Answer
)

class AddQuetionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'lesson_name','master_name',
            'image', 'day'
        )

class AddAnswerForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'4'
            }
        )
    )
    image_answer = forms.ImageField()

    class Meta:
        model = Answer
        fields = (
            'username',
        )