from django import forms
from .models import Post, Category

# Takahashi Shunichi
class PostForm(forms.Form):
    content = forms.CharField(label='ポスト')
    title = forms.CharField(label='作品名')
    author = forms.CharField(label='著者名')

# Takahashi Shunichi
class TagForm(forms.Form):
    data = [[c.id, c.category] for c in Category.objects.all()]
    tag = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=data)


class CommentForm(forms.Form):
    """Form for comment on posts.

    Author:
        Masato Umakoshi
    """
    comment = forms.CharField(label='コメント')
