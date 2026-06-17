from .models import Post
from django import forms

class PostForm(forms.ModelForm):
  class Meta:
    model=Post
    fields=['name','catchphrase','concept','image']
    widgets={
      'name':forms.TextInput(attrs={'placeholder':'name'}),
      'catchphrase':forms.Textarea(attrs={'rows': 3}),
      'concept':forms.Textarea(attrs={'rows': 3}),

    }
    labels={
      'name':'プロトタイプの名称',
      'catchphrase':'解決したい課題',
      'concept':'コンセプト',
      'image':'プロトタイプの画像',

    }
