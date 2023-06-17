from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    color = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'color']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.color = self.cleaned_data.get('color')

        if commit:
            user.save()
            Profile.objects.create(user=user, color=user.color)

        return user