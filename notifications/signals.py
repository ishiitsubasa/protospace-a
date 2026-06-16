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

    Notification.objects.create(
        user=post_author,       # ← recipient から user に変更
        comment=instance,
        # read_at は指定しない → NULLのまま = 未読
    )