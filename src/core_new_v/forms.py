from django import forms

from .models import (
    Question, Answer
)

class AddQuetionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'lesson_name','master_name',
            'iamge', 'day'
        )

class AddAnswerForm(forms.Form):
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
            'username'
        )