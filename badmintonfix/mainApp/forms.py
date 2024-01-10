from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import club,match,player,session

class createClubForm(forms.ModelForm):
    class Meta:
        model = club
        fields = '__all__'
        exclude  = ('clubOrganiser',)

class addScore(forms.ModelForm):
    class Meta:
        model = match
        fields = ('score',)

class addPlayerForm(forms.ModelForm):
    class Meta:
        model = player
        fields =('playerName',)

class addSessionPlayerForm(forms.ModelForm):

    players = forms.ModelMultipleChoiceField(
        queryset=player.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        )

    class Meta:
        model = session
        fields = ('players',)

    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', None)
        session = kwargs.pop('session', None)
        super(addSessionPlayerForm, self).__init__(*args, **kwargs)

        if club:
            excluded_players = session.players.all() if session else []
            #Exclude players not belonging to the club and players that are already in the Session
            self.fields['players'].queryset = player.objects.filter(club = club).exclude(playerName__in=[player.playerName for player in excluded_players])

class deleteSessionPlayerForm(forms.ModelForm):

    players = forms.ModelMultipleChoiceField(
        queryset=player.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        )

    class Meta:
        model = session
        fields = ('players',)

    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', None)
        session = kwargs.pop('session', None)
        super(deleteSessionPlayerForm, self).__init__(*args, **kwargs)

        if club:
            included_players = session.players.all() if session else []
            self.fields['players'].queryset = included_players