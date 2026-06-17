from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse
from .models import Notification


@login_required
def unread_count(request):
    count = Notification.objects.filter(
        user=request.user,
        read_at__isnull=True,
    ).count()
    return JsonResponse({"count": count})


@login_required
@require_POST
def mark_all_read(request):
    updated = Notification.objects.filter(
        user=request.user,
        read_at__isnull=True,
    ).update(read_at=timezone.now())
    return JsonResponse({"marked": updated})


@login_required
@require_POST
def mark_one_read(request, notification_id):
    notification = get_object_or_404(
        Notification, pk=notification_id, user=request.user
    )
    if not notification.is_read:
        notification.read_at = timezone.now()
        notification.save(update_fields=["read_at"])
    return JsonResponse({"ok": True})


@login_required
def notification_list(request):                          # ← 追加
    """通知一覧ページ：未読を既読にしてから表示"""
    notifications = Notification.objects.filter(
        user=request.user,
    ).select_related('comment', 'comment__post', 'comment__user').order_by('-created_at')

    # 一覧を開いたタイミングで全件既読にする
    Notification.objects.filter(
        user=request.user,
        read_at__isnull=True,
    ).update(read_at=timezone.now())

    return render(request, 'notifications/list.html', {
        'notifications': notifications,
    })