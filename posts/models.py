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


class SympathyVote(models.Model):
  VOTE_CHOICES = [('yes', '共感する'), ('maybe', 'どちらとも'), ('no', '共感しない')]

  class Meta:
    db_table = 'sympathy_votes'
    unique_together = ('post', 'user')

  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='sympathy_votes')
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  vote_type = models.CharField(max_length=5, choices=VOTE_CHOICES)
  department = models.CharField(max_length=100, default='未設定')
  created_at = models.DateTimeField(auto_now_add=True)


class PainScore(models.Model):
  class Meta:
    db_table = 'pain_scores'
    unique_together = ('post', 'user')

  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pain_scores')
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  score = models.IntegerField()
  department = models.CharField(max_length=100, default='未設定')
  created_at = models.DateTimeField(auto_now_add=True)
