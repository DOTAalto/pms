from django.urls import path
from vote import views


urlpatterns = [
    path('login/', views.LoginVoteView.as_view(), name="vote-login"),
    path('<int:pk>/', views.VoteView.as_view(), name='vote'),
    path('entry/<int:entry_pk>', views.cast_vote_for_entry, name='vote-entry'),
    path('available-entries/<int:compo_pk>', views.entries_to_vote_for, name='available-entries'),
    path('', views.VoteListView.as_view(), name='vote-list'),
    path('management/', views.VoteManagementView.as_view(), name='vote-management'),
]
