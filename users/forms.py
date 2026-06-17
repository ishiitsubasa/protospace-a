from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
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
        fields = ['email', 'nickname', 'belonging', 'role', 'password1', 'password2']
        widgets = {
            'nickname': forms.TextInput(attrs={'maxlength': '10', 'placeholder': '名前'}),
            'role': forms.TextInput(attrs={'placeholder': '役職'}),
        }

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if len(nickname) > 10:
            raise forms.ValidationError('ニックネームは10文字以内で入力してください。')
        return nickname

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise forms.ValidationError('パスワードは6文字以上で入力してください。')
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワードが一致しません。')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
     # ← これを追加！usernameを除外する
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']