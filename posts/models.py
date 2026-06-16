from django.db import models
from django.conf import settings

class Post(models.Model):
  class Meta:
    db_table='posts'
  name=models.CharField(max_length=100,null=False,blank=False)
  catchphrase=models.TextField(null=False,blank=False)
  concept=models.TextField(null=False,blank=False)
  image=models.ImageField(upload_to='images/',blank=False,null=False)
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
  class Meta:
    db_table = 'likes'
    unique_together = ('user', 'post')
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)
