from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from posts.models import Post

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = post
        comment.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('Posts:detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('Posts:detail', kwargs={'pk': self.kwargs['pk']})