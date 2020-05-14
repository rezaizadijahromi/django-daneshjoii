from django import forms

from .models import Question, Lesson, MasterName, Answer

class AddQuestion(forms.ModelForm):
    # lesson_name = forms.CharField()
    # master_name = forms.CharField()
    # ref_code = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = (
            'lesson_name','master_name',
            'image'
        )

class AddAnswerForm(forms.Form):

    # username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows':'4'
    }))
    image_answer = forms.ImageField()
    
    class Meta:
        model = Answer
        fields = ('username')