from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView,ListView,DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class PostDetailView(DetailView):
  model=Post
  template_name='posts/detail.html'
# Create your views here.



class PostCreateView(CreateView):
  form_class=PostForm
  template_name='posts/create.html'
  success_url=reverse_lazy("Posts:index")

  def form_valid(self,form):
    post=form.save(commit=False)
    post.user = self.request.user
    post.save()
    return super().form_valid(form)

  
