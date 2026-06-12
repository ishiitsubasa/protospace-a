from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView,ListView,DeleteView,DetailView
from django.urls import reverse_lazy
from .models import Post
from django.views.generic.edit import FormMixin
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).select_related('user')
        context['form'] = self.get_form()
        return context



class PostCreateView(CreateView):
  form_class=PostForm
  template_name='posts/create.html'
  success_url=reverse_lazy("Posts:index")

  def form_valid(self,form):
    post=form.save(commit=False)
    post.user = self.request.user
    post.save()
    return super().form_valid(form)

  
