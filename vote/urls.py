from django.urls import path
from vote import views


urlpatterns = [
    path('login/', views.LoginVoteView.as_view(), name="vote-login"),
    path('<int:pk>/', views.VoteView.as_view(), name='vote'),
    path('', views.VoteListView.as_view(), name='vote-list'),
    path('management/', views.VoteManagementView.as_view(), name='vote-management'),
]
