from django.shortcuts import render,redirect
from .models import club,player,match,session
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import createClubForm
from django.contrib import messages
from django.utils import timezone
# Create your views here.

@login_required
def createClub(request):
    form = createClubForm()
    context = {'form': form}

    if request.method == "POST":
        form = createClubForm(request.POST)

        if form.is_valid():
            clubForm = form.save(commit=False)
            clubForm.clubOrganiser = request.user
            clubForm.save()
            return redirect('displayClubs',username = request.user)
        else:
            messages.success(request, form.errors)
            messages.success(request, 'Failed to Create Club')

    return render(request, 'createClub.html',context)

@login_required
def displayClubs(request,username):
    currentUser = request.user
    query = club.objects.filter(clubOrganiser = currentUser)
    context = {
        'query':query,
        'user': currentUser
    }

    return render(request,'displayClubs.html',context)

@login_required
def displayClubDetails(request,username,clubname):
    
    currentUser = request.user
    clubInstance = club.objects.get(clubName = clubname,clubOrganiser = currentUser)
    players = player.objects.filter(club=clubInstance)

    playerNames = [p.playerName for p in players]

    context = {
        'club':clubInstance,
        'players':playerNames,
        'user': currentUser
    }

    return render(request,'displayClubDetails.html',context)


def displaySession(request,username,clubname,sessionid):
    matches = match.objects.filter(session = sessionid)
    matches = [str(match) for match in matches]
    sessionInstance = session.objects.get(sessionID = sessionid)
    date = sessionInstance.date
    context = {
        'matches':matches,
        'user': username,
        'club':clubname,
        'date':date
    }
    return render(request,'displaysession.html',context)


def displayMatch(request,username,clubname,sessionid,matchid):
    matchInstance = match.objects.get(matchID=matchid)
    team1 = matchInstance.team1
    team2 = matchInstance.team2

    team1_names = [player.playerName for player in team1.all()]
    team2_names = [player.playerName for player in team2.all()]

    print(team1_names)

    score = matchInstance.score

    context = {
        'match':matchid,
        'user': username,
        'club':clubname,
        'team1':team1_names,
        'team2':team2_names,
        'score':score
    }
    return render(request,"displayMatch.html",context)