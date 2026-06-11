from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # 確認用パスワードフィールドを追加
    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='パスワード（確認）',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'profile','belonging', 'role', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise forms.ValidationError('パスワードは6文字以上で入力してください。')
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # 2つのパスワードが一致するか確認
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワードが一致しません。')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user