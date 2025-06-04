from django import forms
from users.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    is_teacher = forms.BooleanField(required=False, label="Я являюсь преподавателем")

    class Meta:
        model = User
        fields = ["username", "email", "password"]
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2
 
