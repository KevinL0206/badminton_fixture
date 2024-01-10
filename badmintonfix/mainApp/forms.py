from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import club,match

class createClubForm(forms.ModelForm):
    class Meta:
        model = club
        fields = '__all__'
        exclude  = ('clubOrganiser',)

class addScore(forms.ModelForm):
    class Meta:
        model = match
        fields = ('score',)