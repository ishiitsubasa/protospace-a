from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic
from .forms import DiscussionForm
from posts.models import Post


class DiscussionIndexView(LoginRequiredMixin, View):
    """議題一覧（JSON）"""
    def get(self, request, post_pk):
        topics = Topic.objects.filter(post_id=post_pk).values('id', 'title')
        return JsonResponse({'topics': list(topics)})


class DiscussionCreateView(LoginRequiredMixin, CreateView):
    """議題作成"""
    model = Topic
    form_class = DiscussionForm

    def get_success_url(self):
        return reverse_lazy('Posts:detail', kwargs={'pk': self.kwargs['post_pk']})

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)
