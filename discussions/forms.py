from django import forms
from .models import Topic

class DiscussionForm(forms.ModelForm):
  class Meta:
    model=Topic
    fields=['title']
    widgets={
      'title':forms.TextInput(attrs={'maxlength':'100'})
    }
    labels={
      'title':'議題タイトル'
    }