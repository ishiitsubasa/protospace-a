from django.shortcuts import render
from django.views.generic import ListView, DetailView,DeleteView
from .models import Post
from django.urls import reverse_lazy

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class PostDetailView(DetailView):
  model=Post
  template_name='posts/detail.html'
# Create your views here.
class  PostDeleteView(DeleteView):
  model=Post
  success_url=reverse_lazy('Posts:index')