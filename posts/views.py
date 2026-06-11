from django.shortcuts import render
from django.views.generic import DetailView
from .models import Post

class PostDetailView(DetailView):
  model=Post
  template_name='posts/detail.html'
# Create your views here.