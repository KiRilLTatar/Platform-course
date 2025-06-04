from .models import Test, Question, AnswerOption
from django import forms

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'is_published', 'passing_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desсription': forms.Textarea(attrs={'class': 'form-contol'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control', 'step': 1, 'min': 0, 'max': 100}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'order', 'points']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['text', 'is_correct', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }