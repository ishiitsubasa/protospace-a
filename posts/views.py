from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.views.generic.edit import FormMixin
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.forms import PostForm

class IndexView(ListView):
  model = Post
  template_name = 'posts/index.html'
  context_object_name = 'posts'
  ordering = '-created_at'

class PostCreateView(CreateView):
  form_class=PostForm
  template_name='posts/create.html'
  success_url=reverse_lazy("Posts:index")

  def form_valid(self,form):
    post=form.save(commit=False)
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
        return context

class  PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
  model=Post
  success_url=reverse_lazy('Posts:index')
  form_class=PostForm
  template_name = 'posts/detail.html'

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


  
  
  
    


      
   



  
