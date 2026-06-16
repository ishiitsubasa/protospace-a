from django.db.models.signals import post_save
from django.dispatch import receiver
 
from comments.models import Comment
from .models import Notification
 
 
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    コメントが新規作成されたとき、投稿者へ通知を作成する。
    - 自分自身のコメントは通知しない
    """
    if not created:
        return  # 更新時はスキップ
 
    post_author = instance.post.user
    commenter = instance.user
 
    # 自分の投稿に自分でコメントした場合は通知不要
    if post_author == commenter:
        return
 
    Notification.objects.create(
        recipient=post_author,
        sender=commenter,
        comment=instance,
    )