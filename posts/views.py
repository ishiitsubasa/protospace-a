from django.shortcuts import render
from django.views.generic import CreateView,ListView,DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
# Create your views here.
class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'