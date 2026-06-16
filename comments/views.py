from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
 
from .models import Notification
 

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
    

@login_required
def unread_count(request):
    """
    GET /notifications/unread-count/
    未読通知件数を返す。ポーリングで定期的に叩く。
 
    Response:
        {"count": <int>}
    """
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).count()
    return JsonResponse({"count": count})
 
 
@login_required
@require_POST
def mark_all_read(request):
    """
    POST /notifications/mark-all-read/
    ベルアイコンをクリックした時に全通知を既読にする。
 
    Response:
        {"marked": <int>}   ← 既読にした件数
    """
    updated = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
    ).update(is_read=True)
    return JsonResponse({"marked": updated})
 
 
@login_required
@require_POST
def mark_one_read(request, notification_id):
    """
    POST /notifications/<id>/read/
    個別通知を既読にする（詳細ページ遷移時などに使用）。
 
    Response:
        {"ok": true}
    """
    notification = get_object_or_404(
        Notification, pk=notification_id, recipient=request.user
    )
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return JsonResponse({"ok": True})