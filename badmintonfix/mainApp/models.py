from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.
def get_today():
    return timezone.now().date()

class club(models.Model):
    clubName = models.CharField(max_length = 255)
    clubOrganiser = models.ForeignKey(User,on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['clubName', 'clubOrganiser'], name='unique_club')
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
    club = models.ForeignKey(club,on_delete=models.CASCADE)
    date = models.DateField(default = get_today)
    players = models.ManyToManyField(player)

    def __str__(self):
        return str(self.date)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sessionID', 'club'], name='unique_session')
        ]


class match(models.Model):
    matchID = models.AutoField(primary_key=True)
    session = models.ForeignKey(session,on_delete=models.CASCADE)
    team1 = models.ManyToManyField(player, related_name='team1')
    team2 = models.ManyToManyField(player, related_name='team2')
    score = models.CharField(max_length = 255, default = '00-00')
    completed = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['matchID', 'session'], name='unique_match'),
        ]

    

        