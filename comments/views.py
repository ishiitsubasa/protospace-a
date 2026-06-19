from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from notifications.models import Notification

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        form.instance.user = self.request.user
        form.instance.post = post

        response = super().form_valid(form)  # ここでcommentが1回だけ保存される

        # 自分の投稿へのコメントは通知しない
        if post.user != self.request.user:
            Notification.objects.get_or_create(
                comment=self.object,
                defaults={'user': post.user}
            )

        return response

    def form_invalid(self, form):
        return redirect('discussions:detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('discussions:detail', kwargs={'pk': self.kwargs['pk']})