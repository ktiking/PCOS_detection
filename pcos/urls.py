# get the path function to make URLs
from django.urls import path
# get all our view functions
from . import views

# this is where we tell Django what URLs to use
urlpatterns = [
    # the main page
    path('', views.home_view, name='home'),
    # where users can log in
    path('login/', views.login_view, name='login'),
    # where new users can sign up
    path('signup/', views.signup_view, name='signup'),
    # where users can log out
    path('logout/', views.logout_view, name='logout'),
    # where users can make predictions
    path('prediction/', views.prediction_form_view, name='prediction_form'),
    # where users can see stats
    path('statistics/', views.statistics_view, name='statistics'),
] 