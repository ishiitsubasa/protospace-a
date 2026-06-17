from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Like


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    ordering = '-created_at'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        for post in qs:
            post.liked_by_user = post.is_liked_by(user)
        return qs


@require_POST
def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes_count()})
