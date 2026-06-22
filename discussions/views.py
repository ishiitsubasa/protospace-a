from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import View, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic
from .forms import DiscussionForm
from posts.models import Post
from comments.forms import CommentForm
from comments.models import Comment

class DiscussionIndexView(LoginRequiredMixin, View):
    """議題一覧（JSON）"""
    def get(self, request, post_pk):
        topics = Topic.objects.filter(post_id=post_pk).values('id', 'title')
        return JsonResponse({'topics': list(topics)})


class DiscussionCreateView(LoginRequiredMixin, CreateView):
    """議題作成"""
    model = Topic
    form_class = DiscussionForm
    success_url = reverse_lazy('Posts:detail')
    
    template_name = 'discussions/create.html'

    def get_success_url(self):
        return reverse_lazy('Posts:detail', kwargs={'pk': self.kwargs['post_pk']})

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
        ctx['comments'] = Comment.objects.filter(topic=self.object)
        ctx['form'] = CommentForm()
        return ctx
     
     