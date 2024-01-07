from . import views
from django.urls import path

urlpatterns = [
    path('',views.startPageRedirect, name = 'redirect'),
    path('register/', views.register,name = 'register'),
    path('login/',views.loginUser, name = 'login'),
    path('home/',views.home, name = 'home'),
    path('logout/',views.logoutUser, name = 'logout')

]
