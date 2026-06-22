from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if password and len(password) < 6:
            raise ValidationError('パスワードは6文字以上で入力してください。')
        
        # ← インスタンス生成を1つにまとめました！
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
   
    Belonging_CHOICES = [
        ('engineering', 'エンジニアリング部'),
        ('sales', '営業部'),
        ('marketing', 'マーケティング部'),
        ('hr', '人事部'),
        ('finance', '経理部'),
        # 必要な部署を追加
    ]

    email = models.EmailField(unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=10, blank=False, null=False)
    belonging = models.CharField(
        max_length=100,
        choices=Belonging_CHOICES,
        blank=False,
        null=False)
    role = models.CharField(max_length=15,blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        
    def clean(self):
        super().clean()
        if self.password and len(self.password) < 6:  # ← not self.passwordを削除
            raise ValidationError({'password': 'パスワードは6文字以上で入力してください。'})
        

