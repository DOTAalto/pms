from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class LoginView(DjangoLoginView):
    success_url = reverse_lazy('party')

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('party'))