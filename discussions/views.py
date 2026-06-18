from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView,CreateView
from .models import Topic
from django.shortcuts import get_object_or_404,redirect
from posts.models import Post
from comments.models import Count
from django .forms import DiscussionTopicForm
from django.contrib.auth.mixins import LoginRequiredMixin





class DiscussionCreateView(LoginRequiredMixin, CreateView):
    """議題作成"""
    model = Topic
    form_class = DiscussionTopicForm
    success_url = reverse_lazy('Posts:detail')
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)




     
     
     

     
