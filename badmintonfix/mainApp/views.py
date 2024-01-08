from django.shortcuts import render,redirect
from .models import club,player,match
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
    context = {'query':query}

    return render(request,'displayClubs.html',context)

def displayClubDetails(request,username,clubname):
    
    currentUser = request.user
    club = club.objects.get(clubName = clubname,clubOrganiser = currentUser)
    players = player.objects.filter(club=club)

    playerNames = [p.playerName for p in players]

    context = {
        'club':club,
        'players':playerNames
    }

    return render(request,'displayClubDetails.html',context)

def displaySession(request,username,clubname,sessionid):
    matches = match.objects.filter(session = sessionid)
    context = {
        'matches':matches
    }
    return render(request,'displaysession.html',context)

def displayMatch(request,username,clubname,sessionid,matchID):
    match = match.objects.get(matchID=matchID)
    context = {
        'match':match
    }
    return render(request,"displayMatch.html",context)