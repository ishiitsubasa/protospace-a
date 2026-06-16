from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Like
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.views.generic.edit import FormMixin
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'

  def get_queryset(self):
    sort = self.request.GET.get('sort', 'new')
    qs = Post.objects.all()
    if sort == 'likes':
      qs = qs.annotate(like_count=models.Count('likes')).order_by('-like_count', '-created_at')
    else:
      qs = qs.order_by('-created_at')
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    sort = self.request.GET.get('sort', 'new')
    context['current_sort'] = sort
    if self.request.user.is_authenticated:
      liked_ids = set(Like.objects.filter(user=self.request.user).values_list('post_id', flat=True))
      context['liked_post_ids'] = liked_ids
    else:
      context['liked_post_ids'] = set()
    if sort == 'new':
      two_weeks_ago = timezone.now() - timedelta(weeks=2)
      trending = (
        Post.objects
        .annotate(recent_likes=Count('likes', filter=Q(likes__created_at__gte=two_weeks_ago)))
        .filter(recent_likes__gt=0)
        .order_by('-recent_likes', '-created_at')[:3]
      )
      context['trending_posts'] = list(trending)
      context['trending_ids'] = {p.pk for p in context['trending_posts']}
    else:
      context['trending_posts'] = []
      context['trending_ids'] = set()
    return context

class PostDetailView(DetailView):
  model=Post
  template_name='posts/detail.html'
# Create your views here.



class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('Posts:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)



class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).select_related('user')
        context['form'] = self.get_form()
        context['like_count'] = self.object.likes.count()
        context['user_liked'] = (
            self.request.user.is_authenticated and
            Like.objects.filter(user=self.request.user, post=self.object).exists()
        )
        return context

class  PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
  model=Post
  success_url=reverse_lazy('Posts:index')


  def test_func(self):
    post=self.get_object()

    return post.user==self.request.user


class PostUpdateView(LoginRequiredMixin, UpdateView):
  model = Post
  form_class = PostForm
  template_name = 'posts/update.html'

  def dispatch(self, request, *args, **kwargs):
      post = self.get_object()
        # 自分の投稿でなければトップへ
      if post.user != request.user:
          return redirect('Posts:index')
      return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
      post = form.save(commit=False)
        # 画像が送られていない場合、既存画像を保持
      if not self.request.FILES.get('image'):
          post.image = self.get_object().image
          post.save()
      return super().form_valid(form)

  def get_success_url(self):
      # 編集成功後は詳細ページへ
      return reverse_lazy('Posts:detail', kwargs={'pk': self.object.pk})


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        return JsonResponse({'error': 'forbidden'}, status=403)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})

