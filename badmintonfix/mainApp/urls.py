from . import views
from django.urls import path

urlpatterns = [
    path('<str:username>/createClub/',views.createClub,name='createClub'),
    path('<str:username>/',views.displayClubs,name = 'displayClubs'),
    path('<str:username>/<str:clubname>/',views.displayClubDetails,name = 'displayClubDetails'),
    path('<str:username>/<str:clubname>/<int:sessionid>',views.displaySession,name = 'displaysession'),
    path('<str:username>/<str:clubname>/<int:sessionid>/<int:matchid>',views.displayMatch,name = 'displayMatch'),
    path('<str:username>/<str:clubname>/<int:sessionid>/createMatch',views.createMatch,name='createMatch'),
    path('<str:username>/<str:clubname>/allSessions',views.displayAllSessions,name = 'displayAllSessions'),
    path('<str:username>/<str:clubname>/createSession',views.createSession,name='createSession'),
]