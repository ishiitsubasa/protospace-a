from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from notifications.models import Notification
from discussions.models import Topic

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        form.instance.user = self.request.user
        form.instance.post = post

        topic_pk = self.kwargs.get('topic_pk')
        if topic_pk:
            form.instance.topic = get_object_or_404(Topic, pk=topic_pk)

        response = super().form_valid(form)
        if post.user != self.request.user:
            Notification.objects.get_or_create(
                comment=self.object,
                defaults={'user': post.user}
            )
        return response

    def form_invalid(self, form):
        topic_pk = self.kwargs.get('topic_pk')
        if topic_pk:
            return redirect('discussions:detail', pk=topic_pk)
        return redirect('Posts:detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        topic_pk = self.kwargs.get('topic_pk')
        if topic_pk:
            return reverse('discussions:detail', kwargs={'pk': topic_pk})
        return reverse('Posts:detail', kwargs={'pk': self.kwargs['pk']})