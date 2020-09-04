from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def comment_post(request, post_id, user_id, comment):
    """Posting comment function.

    Author:
        Masato Umakoshi
    """
    return HttpResponse(
        f"Post id: {post_id}, User id: {user_id}, comment content: {comment}")
