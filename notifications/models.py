from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Meta:
        db_table = 'notifications'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    comment = models.OneToOneField('comments.Comment', on_delete=models.CASCADE)  # 文字列参照に変更
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_read(self):
        return self.read_at is not None