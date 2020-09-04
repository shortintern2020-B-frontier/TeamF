from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

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
    return HttpResponse(
        f"Post id: {post_id}, User id: {user_id}, comment content: {comment}")
