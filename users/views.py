from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model, logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm, UserUpdateForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('Posts:index')
    template_name = 'users/sign_up.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserPageView(ListView):
    model = Post
    template_name = 'users/mypage.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        self.user = get_object_or_404(get_user_model(), pk=user_id)
        return Post.objects.filter(user=self.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.user
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        return reverse_lazy('users:mypage', kwargs={'pk': self.request.user.pk})


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('Posts:index')
    template_name = 'users/user_delete.html'


    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)