from django.db.models.signals import post_save
from django.dispatch import receiver

from comments.models import Comment
from .models import Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if not created:
        return

    post_author = instance.post.user
    commenter = instance.user

    if post_author == commenter:
        return

    # ↓ 既に通知が存在する場合は作らない
    Notification.objects.get_or_create(
        comment=instance,
        defaults={'user': post_author}
    )