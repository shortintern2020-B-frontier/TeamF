from django import forms
from .models import Post, Category

# Takahashi Shunichi
class PostForm(forms.Form):
    content = forms.CharField(label='ポスト')
    title = forms.CharField(label='作品名')
    author = forms.CharField(label='著者名')


class TagForm(forms.Form):
    data = [[c.id, c.category] for c in Category.objects.all()]
    # for c in Category.objects.all():
    #     data.append([c.id, c.category])
    tag = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=data)

    class Meta:
        initial = [category.category for category in Category.objects.filter()]


class CommentForm(forms.Form):
    """Form for comment on posts.

    Author:
        Masato Umakoshi
    """
    comment = forms.CharField(label='コメント')
