"""
URL configuration for pms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from party import views
from accounts.views import SignUpView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<slug:slug>', views.PartyDetailView.as_view(), name="party-detail"),
    path('<int:compo_pk>/submit/', views.CreateEntryView.as_view(), name="submit-entry"),
    path('entry/<int:pk>', views.UpdateEntryView.as_view(), name="update-entry"),
    path('party/', views.PartyList.as_view(), name='party-list'),

    path("login/", LoginView.as_view(), name='login'),
    path("vote/", include("vote.urls")),
    path("beamer/", include("beamer.urls")),
]
