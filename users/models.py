from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
  def create_user(self,email,nickname,password=None,**extra_fields):
    if not email:
      raise ValueError('Users must have an email address')
    if password and len(password) < 8:
       raise ValidationError('パスワードは8文字以上で入力してください。')
    
    user = self.model(email=self.normalize_email(email),
                       nickname=nickname, 
                       **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=10, blank=False, null=False)
    profile = models.CharField(max_length=100,blank=False, null=False)
    belonging = models.TextField(blank=False, null=False)
    role = models.CharField(max_length=15,blank=False, null=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'users'
# Create your models here.
