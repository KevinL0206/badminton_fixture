from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
def get_today():
    return timezone.now().date()

class club(models.Model):
    clubName = models.CharField(max_length = 255)
    clubOrganiser = models.ForeignKey(User,on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['clubName', 'clubOrganiser'], name='unique_field1_field2')
        ]

    def __str__(self):
        return f"{self.clubName} - {self.clubOrganiser.username}"


class player(models.Model):
    playerName = models.CharField(max_length = 255,primary_key = True)
    club = models.ForeignKey(club,on_delete=models.CASCADE)
    inGameFlag = models.BooleanField(default = False)
    elo = models.IntegerField(default = 1200)

class session(models.Model):
    sessionID = models.AutoField(primary_key=True)
    date = models.DateField(default = get_today)
    players = models.ManyToManyField(player)

    def __str__(self):
        return self.date


class match(models.Model):
    matchID = models.AutoField(primary_key=True)
    session = models.ForeignKey(session,on_delete=models.CASCADE)
    team1 = models.ManyToManyField(player, related_name='team1')
    team2 = models.ManyToManyField(player, related_name='team2')
    score = models.CharField(max_length = 255, default = '00-00')
    completed = models.BooleanField(default=False)

    def clean(self):
        # Ensure that no player is in both team1 and team2
        common_players = set(self.team1.all()) & set(self.team2.all())
        if common_players:
            raise ValueError("A player cannot be in both team1 and team2.")
        if self.team1.count() > 2 or self.team2.count() > 2:
            raise ValueError("Each team can have a maximum of 2 players.")
        
    def __str__(self):
        team1_names = ', '.join([player.playerName for player in self.team1.all()])
        team2_names = ', '.join([player.playerName for player in self.team2.all()])
        return f"{self.matchID} - Team1: {team1_names} - Team2: {team2_names} - {self.completed}"