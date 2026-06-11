from django.shortcuts import render, redirect
from django.views.generic import UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class PostDetailView(DetailView):
  model=Post
  template_name='posts/detail.html'

class UpdateView(LoginRequiredMixin, UpdateView):
  model = Post
  form_class = PostForm
  template_name = 'posts/update.html'

  def dispatch(self, request, *args, **kwargs):
      post = self.get_object()
        # 自分の投稿でなければトップへ
      if post.user != request.user:
          return redirect('posts:index')
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