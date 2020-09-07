# from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Book, Comment, Post, User


# Takahashi Shunichi
def index(request):
    post = Post.objects.filter(is_deleted=False)

    params = {"title": "ポスト一覧", "post": post}
    return render(request, "posts/index.html", params)


# Takahashi Shunichi
def detail(request, num):
    post = Post.objects.get(id=num)
    comments = Comment.objects.filter(post_id=num)
    params = {
        "title": "ポスト詳細",
        "post": post,
        "comments": comments,
        "form": CommentForm
    }
    return render(request, "posts/detail.html", params)


# Takahashi Shunichi
@transaction.atomic
def create(request):
    if request.method == "POST":
        content = (request.POST["content"], )
        title = (request.POST["title"], )
        author = (request.POST["author"], )

        book = Book(title=title, author=author)  # すでに存在するなら追加しない
        book.save()
        user = User.objects.get(id=request.user.id)
        post = Post(user_id=user, content=content, book_id=book)
        post.save()

        return redirect(to="/posts")
    params = {"title": "ポスト投稿", "form": PostForm()}
    return render(request, "posts/create.html", params)


# Takahashi Shunichi
@transaction.atomic
def edit(request, num):
    post = Post.objects.get(id=num)
    book_id = post.id
    book = Book.objects.get(id=book_id)
    initial_dict = {
        "content": post.content,
        "title": book.title,
        "author": book.author
    }

    if request.method == "POST":
        content = (request.POST["content"], )
        title = (request.POST["title"], )
        author = (request.POST["author"], )

        book.title = title
        book.author = author
        book.save()
        post.content = content
        post.save()
        return redirect(to="/posts")

    params = {
        "title": "ポスト編集",
        "id": num,
        "form": PostForm(initial=initial_dict)
    }
    return render(request, "posts/edit.html", params)


# Takahashi Shunichi
@transaction.atomic
def delete(request, num):
    post = Post.objects.get(id=num)
    if request.method == "POST":
        post.is_deleted = True
        post.save()
        return redirect(to="/posts")

    params = {"title": "ポスト削除", "id": num, "post": post}
    return render(request, "posts/delete.html", params)


@transaction.atomic
def comment_create(request, num):
    """Posting comment function.

    TODO:
        handle
            * Not logged in user
            * Not post request

    Author:
        Masato Umakoshi
    """
    # If not post, raise 404
    if request.method != "POST":
        raise Http404("Hogehoge")

    # This may be too naive
    user_id = request.user.id
    content = request.POST["content"]
    comment = Comment(
        user_id=User.objects.get(pk=user_id),
        post_id=Post.objects.get(pk=num),
        content=content,
    )
    comment.save()
    # post_id may be post.id??
    # return HttpResponseRedirect(reverse("posts:show", args=(num, )))
    return redirect(to="/posts")
