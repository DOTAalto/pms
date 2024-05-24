from django.urls import path
from vote import views


urlpatterns = [
    path('login/', views.LoginVoteView.as_view(), name="vote-login"),
    path('', views.VoteView.as_view(), name='vote')
]
