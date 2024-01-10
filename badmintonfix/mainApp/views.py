from django.shortcuts import render,redirect
from .models import club,player,match,session
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import createClubForm,addScore,addPlayerForm,addSessionPlayerForm,deleteSessionPlayerForm
from django.contrib import messages
from django.utils import timezone
from .functions import calcGameElo
# Create your views here.

@login_required
def createClub(request,username):
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

    form = addPlayerForm()

    if request.method == "POST":
        form = addPlayerForm(request.POST)

        if form.is_valid():
            playername = form.cleaned_data['playerName']
            newPlayerInstance = player.objects.create(
                playerName = playername,
                club = clubInstance
            )
            return redirect('displayClubDetails', username=username, clubname=clubname)
        else:
            messages.success(request, form.errors)
            messages.success(request, 'Failed to Add Player')

    context = {
        'form':form,
        'club':clubname,
        'players':playerNames,
        'user': currentUser
    }

    return render(request,'displayClubDetails.html',context)

def displayAllSessions(request,username,clubname):
    userInstance = User.objects.get(username = username)
    clubInstance = club.objects.get(clubName = clubname, clubOrganiser = userInstance)
    sessions = session.objects.filter(club=clubInstance)

    context = {
        'user': username,
        'club':clubname,
        'sessions':sessions
    }

    return render(request,'displayAllSessions.html',context)

def displaySession(request,username,clubname,sessionid):
    userInstance = User.objects.get(username = username)
    clubInstance = club.objects.get(clubName = clubname, clubOrganiser = userInstance)
    matches = match.objects.filter(session = sessionid)
    matchesStr = [str(match) for match in matches]
    sessionInstance = session.objects.get(sessionID = sessionid)
    date = sessionInstance.date

    session_players = sessionInstance.players
    player_names = [player.playerName for player in session_players.all()]
    form = addSessionPlayerForm(club = clubInstance, session = sessionInstance)
    deletePlayerForm = deleteSessionPlayerForm(club = clubInstance, session = sessionInstance)

    if request.method == "POST":

        add_button_clicked = 'Add_Player_to_Session' in request.POST
        delete_button_clicked = 'Delete_Player_From_Session' in request.POST

        if add_button_clicked:
            form = addSessionPlayerForm(request.POST, club=clubInstance, session=sessionInstance)
            if form.is_valid():

                players = form.cleaned_data['players']
                print(1)

                for player in players:
                    sessionInstance.players.add(player)
                
                return redirect('displaysession', username = username,clubname = clubname,sessionid = sessionid)
            else:
                messages.success(request, form.errors)
                messages.success(request,'Failed to Add Players')

        elif delete_button_clicked:
            deletePlayerForm = deleteSessionPlayerForm(request.POST, club=clubInstance, session=sessionInstance)
            
            if deletePlayerForm.is_valid():

                players = deletePlayerForm.cleaned_data['players']
                print(2)
                for player in players:
                    sessionInstance.players.remove(player)
                
                return redirect('displaysession', username = username,clubname = clubname,sessionid = sessionid)
            else:
                messages.success(request, form.errors)
                messages.success(request,'Failed to Remove Players')

    context = {
        'form':form,
        'deleteplayerform':deletePlayerForm,
        'matches':matches,
        'user': username,
        'club':clubname,
        'date':date,
        'session':sessionid,
        'players': player_names
    }
    return render(request,'displaysession.html',context)

def displayMatch(request,username,clubname,sessionid,matchid):
    matchInstance = match.objects.get(matchID=matchid)
    organiserInstance = User.objects.get(username=username)
    clubInstance = club.objects.get(clubName = clubname, clubOrganiser = organiserInstance)

    team1 = matchInstance.team1
    team2 = matchInstance.team2

    #Get player names
    team1_names = [player.playerName for player in team1.all()]
    team2_names = [player.playerName for player in team2.all()]

    score = matchInstance.score

    form = addScore()
    if request.method == "POST" :
        form = addScore(request.POST)

        if form.is_valid() and not matchInstance.completed:
            score = form.cleaned_data['score']

            #Get Match Score
            team1Score, team2Score = map(int, score.split('-'))

            #Calculate which team won
            winloss = []
            if team1Score > team2Score:
                winloss = [1,0]
            elif team2Score > team1Score:
                winloss = [0,1]

            matchInstance.score = score
            matchInstance.completed = True
            matchInstance.save()
            
            #Calculate new ELO rating for each player
            playerOneNewElo,playerTwoNewElo,playerThreeNewElo,playerFourNewElo = calcGameElo(team1,team2,winloss)

            playerOneInstance = player.objects.get(playerName = team1_names[0],club = clubInstance)
            playerTwoInstance = player.objects.get(playerName = team1_names[1],club = clubInstance)
            playerThreeInstance = player.objects.get(playerName = team2_names[0],club = clubInstance)
            playerFourInstance = player.objects.get(playerName = team2_names[1],club = clubInstance)
            
            
            #Update player ELO
            playerOneInstance.elo = playerOneNewElo
            playerOneInstance.inGameFlag = False
            playerOneInstance.save()

            playerTwoInstance.elo = playerTwoNewElo
            playerTwoInstance.inGameFlag = False
            playerTwoInstance.save()

            playerThreeInstance.elo = playerThreeNewElo
            playerThreeInstance.inGameFlag = False
            playerThreeInstance.save()

            playerFourInstance.elo = playerFourNewElo
            playerFourInstance.inGameFlag = False
            playerFourInstance.save()
        else:
            messages.success(request, form.errors)
            if matchInstance.completed:
                messages.success(request, 'Score Has already Been Added')
            else:
                messages.success(request, 'Failed to Add Score')


    context = {
    'form':form,
    'match':matchid,
    'user': username,
    'club':clubname,
    'team1':team1_names,
    'team2':team2_names,
    'score':score,
    'session':sessionid
    }

    return render(request,"displayMatch.html",context)

@login_required
def createMatch(request,username,clubname,sessionid):
    organiserInstance = User.objects.get(username=username)
    clubInstance = club.objects.get(clubName = clubname, clubOrganiser = organiserInstance)
    sessionInstance = session.objects.get(sessionID=sessionid, club = clubInstance)
    freePlayers = list(sessionInstance.players.filter(inGameFlag = False).order_by('elo'))
    print(freePlayers)
    if len(freePlayers) <4:
        messages.success(request, 'Not Enough Players')
        return redirect('displaysession',username = username,clubname = clubname,sessionid = sessionid)
    else:
        matchPlayers = []
        for _ in range(4):
            if freePlayers:
                player = freePlayers.pop()
                player.inGameFlag = True
                player.save()
                matchPlayers.append(player)

        newMatchInstance = match.objects.create(
            session = sessionInstance,
            score = '00-00'
        )

        newMatchInstance.team1.add(matchPlayers[0],matchPlayers[3])
        newMatchInstance.team2.add(matchPlayers[1],matchPlayers[2])

        return redirect('displayMatch',username=username,clubname = clubname, sessionid = sessionid,matchid = newMatchInstance.matchID)

@login_required
def createSession(request,username,clubname):
    userInstance = User.objects.get(username=username)
    clubInstance = club.objects.get(clubName = clubname, clubOrganiser = userInstance)
    date = timezone.now().date()

    if session.objects.filter(club = clubInstance,date=date):
        messages.success(request,'Session Already Exists')
    else:
        newSessionInstance = session.objects.create(
            club = clubInstance,
        )

    return redirect('displayAllSessions', username=username, clubname=clubname)


