from . import views
from django.urls import path

urlpatterns = [
    path('createClub/',views.createClub,name='createClub'),
    path('<str:username>/',views.displayClubs,name = 'displayClubs'),
    path('<str:username>/<str:clubname>/',views.displayClubDetails,name = 'displayClubDetails')
]