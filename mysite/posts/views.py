from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Comment


# Create your views here.
def show(request, post_id):
    """Showing single post.

    Author:
        Masato Umakoshi
    """
    # post = Post.objects.get(pk=post_id)
    # comments = Comment.objects.filter(post__id=post_id)
    comments = Comment.objects.all()

    template = loader.get_template('posts/show.html')
    context = {
        # 'post': post,
        'comments': comments
    }
    return HttpResponse(template.render(context, request))


def comment_post(request, post_id, user_id, comment):
    """Posting comment function.

    Author:
        Masato Umakoshi
    """
    comment = Comment(
        user=User.get(pk=user_id),
        # post=Post.get(pk=post_id),
        comment=comment
    )
    comment.save()
    # post_id may be post.id??
    return HttpResponseRedirect(reverse('posts:show', args=(post_id,)))
