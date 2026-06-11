from django.urls import reverse_lazy
from django.contrib.auth import login,get_user_model
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from posts.models import Post
from django.views.generic import CreateView
from .forms import CustomUserCreationForm



class SignUpView(CreateView):
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('Post:index')
  template_name = 'users/sign_up.html'


class UserPageView(ListView):
  model = Post
  template_name = 'users/mypage.html'
  context_object_name = 'posts'

  def get_queryset(self):
    user_id = self.kwargs.get('pk')
    self.user = get_object_or_404(get_user_model(), pk=user_id)
    return Post.objects.filter(user=self.user).order_by('-created_at')
  
  def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.user
        return context


# Create your views here.
