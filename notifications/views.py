from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Notification


@login_required
def unread_count(request):
    """
    GET /notifications/unread-count/
    read_at が NULL のもの = 未読として件数を返す
    """
    count = Notification.objects.filter(
        user=request.user,
        read_at__isnull=True,   # ← is_read=False の代わり
    ).count()
    return JsonResponse({"count": count})


@login_required
@require_POST
def mark_all_read(request):
    """
    POST /notifications/mark-all-read/
    read_at が NULL のものに現在時刻をセット → 既読にする
    """
    updated = Notification.objects.filter(
        user=request.user,
        read_at__isnull=True,           # ← 未読のものだけ
    ).update(read_at=timezone.now())    # ← Trueではなく現在時刻をセット
    return JsonResponse({"marked": updated})


@login_required
@require_POST
def mark_one_read(request, notification_id):
    """
    POST /notifications/<id>/read/
    個別通知を既読にする
    """
    notification = get_object_or_404(
        Notification, pk=notification_id, user=request.user
    )
    if not notification.is_read:        # ← @property で判定
        notification.read_at = timezone.now()
        notification.save(update_fields=["read_at"])
    return JsonResponse({"ok": True})