from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic.edit import FormMixin
from comments.forms import CommentForm
from comments.models import Comment

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class DetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = self.get_form()
        return context
