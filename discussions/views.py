from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from .models import Topic
from django.shortcuts import get_object_or_404
from posts.models import Post
from .forms import DiscussionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import CommentForm


class DiscussionCreateView(LoginRequiredMixin, CreateView):
    """議題作成"""
    model = Topic
    form_class = DiscussionForm
    success_url = reverse_lazy('Posts:detail')
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)


class DiscussionDetailView(DetailView):
    model = Topic
    template_name = 'discussions/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['discussions'] = self.object        # Topic
        ctx['post'] = self.object.post          # Post（include先が使う）
        ctx['comments'] = ...
        ctx['form'] = CommentForm()
        return ctx
     
     
     

     
