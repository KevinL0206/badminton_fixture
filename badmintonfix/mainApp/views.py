from django.shortcuts import render,redirect
from .models import club
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import createClubForm
from django.contrib import messages
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
    query = club.objects.all().filter(clubOrganiser = currentUser)
    context = {'query':query}

    return render(request,'displayClubs.html',context)

def displayClubDetails(request):

    return render(request,'displayClubDetails.html')

