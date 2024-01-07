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
    elo = models.IntegerField(default = 0)

class session(models.Model):
    date = models.DateField(default = get_today,primary_key=True)
    players = models.ManyToManyField(player)


class match(models.Model):
    matchID = models.AutoField(primary_key=True)
    session = models.ForeignKey(session,on_delete=models.CASCADE,default=get_today)
    team1 = models.ManyToManyField(player, related_name='team1')
    team2 = models.ManyToManyField(player, related_name='team2')
    score = models.IntegerField()

    def clean(self):
        # Ensure that no player is in both team1 and team2
        common_players = set(self.team1.all()) & set(self.team2.all())
        if common_players:
            raise ValueError("A player cannot be in both team1 and team2.")
        if self.team1.count() > 2 or self.team2.count() > 2:
            raise ValueError("Each team can have a maximum of 2 players.")