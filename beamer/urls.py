from django.urls import path

from beamer import views


urlpatterns = [
    path('management/', views.ControlBeamerView.as_view(), name='control-beamer'),
]
