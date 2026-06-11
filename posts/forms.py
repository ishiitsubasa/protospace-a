from .models import Post
from django import forms

class PostForm(forms.ModelForm):
  class Meta:
    model=Post
    fields=['name','catchphrase','concept','image']
    widgets={
      'name':forms.TextInput(attrs={'placeholder':'name'}),
      'catchphrase':forms.Textarea(attrs={'placeholder': 'Text', 'rows': 10}),
      'concept':forms.Textarea(attrs={'placeholder': 'Text', 'rows': 10}),

    }
    labels={
      'name':'プロトタイプの名称',
      'catchphrase':'キャッチコピー',
      'concept':'コンセプト',
      'image':'プロトタイプの画像',

    }
