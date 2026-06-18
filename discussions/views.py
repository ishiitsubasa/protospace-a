from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView,CreateView
from .models import Topic
from django.shortcuts import get_object_or_404,redirect
from posts.models import Post
from comments.models import Count
from django .forms import TopicForm
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class DiscussionIndexView(ListView):
  model=Topic
  template_name='discussions/index.html'
  context_object_name='topics'
  def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return (
            Topic.objects
            .filter(post=self.post)
            .annotate(comment_count=Count('comments'))
            .order_by('-comment_count', '-created_at')
        )
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['post'] = self.post
      context['topic_form'] = TopicForm()

      Topic_id=self.request.GET.get('topic')
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['post'] = self.post
    context['topic_form'] = TopicForm()
    return context

class DiscussionCreateView(LoginRequiredMixin, CreateView):
    """議題作成"""
    model = Topic
    form_class = TopicForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)



     
     
     

     
