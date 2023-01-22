from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing,name="landing"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('Home/', views.Home, name="Home"),
    path('Profile/', views.Profile),
    path('Bookmarks/', views.Bookmarks, name="Bookmarks"),
    path('MyExperiences/', views.MyExperiences),
    path('logout/', views.logout_user, name="logout"),
    path('password_reset/', views.password_reset, name="password_reset"),
]