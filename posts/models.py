from django.db import models
from django.conf import settings

class Post(models.Model):
  class Meta:
    db_table='posts'
  name=models.CharField(null=False,blank=False)
  catchphrase=models.TextField(null=False,blank=False)
  concept=models.TextField(null=False,blank=False)
  image=models.ImageField(upload_to='images/',blank=False,null=False)
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  

# Create your models here.
