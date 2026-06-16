from django.db import models
from django.conf import settings


class Comment(models.Model):
    class Meta:
        db_table = 'comments'

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    post       = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=False)
    text       = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  