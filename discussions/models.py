from django.db import models
from django.conf import settings


class Topic(models.Model):
    class Meta:
        db_table = 'topics'
        ordering = ['-created_at']

    post       = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='topics')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='created_by_id')
    title      = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()