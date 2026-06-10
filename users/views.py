from django.urls import reverse_lazy
from django.contrib.auth import login,get_user_model
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from posts.models import Post
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('Post:index')
  template_name = 'users/sign_up.html'





# Create your views here.