from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Book, Post, Wokashi, Ahare, Bookmark, Comment, Nice
from .forms import PostForm
from django.db import transaction
import urllib.parse

# from .models import User

import requests
import time

RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = "1065776451953533134"
def get_book_cover_path(title, author):
    encoded_title = urllib.parse.quote(str(title))
    encoded_author = urllib.parse.quote(str(author))
    response = requests.get("{}?format=json&applicationId={}&title={}&author={}".format(RAKUTEN_BOOKS_API_URL, RAKUTEN_APP_ID, encoded_title, encoded_author))
    cover_path = ''
    if response.status_code != requests.codes.ok:
        cover_path = 'Requests failed'
    elif response.json()["count"] == 0:
        cover_path = 'No book found'
    else:
        cover_path = response.json()["Items"][0]["Item"]["largeImageUrl"]
    return cover_path

# Takahashi Shunichi
def index(request):
    post = Post.objects.filter(is_deleted=False)

    params = {
        'title': 'ポスト一覧',
        'post': post,
    }
    return render(request, 'posts/index.html', params)

# Takahashi Shunichi
def detail(request, num):
    post = Post.objects.get(id=num)
    params = {
        'title': 'ポスト詳細',
        'post': post,
    }
    return render(request, 'posts/detail.html', params)

# Takahashi Shunichi
@transaction.atomic
def create(request):
    if (request.method == 'POST'):
        content = request.POST['content'],
        title = request.POST['title'],
        author = request.POST['author'],

        # cover_path = ''
        cover_path = get_book_cover_path(title, author)
        time.sleep(1)

        if cover_path == 'No book found':
            book = Book(title=title, author=author) #すでに存在するなら追加しない
        else:
            book = Book(title=title, author=author, cover_path=cover_path) #すでに存在するなら追加しない
        book.save()
        user = User.objects.get(id=request.user.id)
        post = Post(user_id=user, content=content, book_id=book)
        post.save()

        return redirect(to='/posts')
    params = {
        'title': 'ポスト投稿',
        'form': PostForm(),
    }
    return render(request, 'posts/create.html', params)

# Takahashi Shunichi
@transaction.atomic
def edit(request, num):
    post = Post.objects.get(id=num)
    book_id = post.id
    book = Book.objects.get(id=book_id)
    initial_dict = {
        'content': post.content,
        'title': book.title,
        'author': book.author,
    }

    if (request.method == 'POST'):
        content = request.POST['content'],
        title = request.POST['title'],
        author = request.POST['author'],

        book.title = title
        book.author = author
        book.save()
        post.content = content
        post.save()
        return redirect(to='/posts')

    params = {
        'title': 'ポスト編集',
        'id': num,
        'form': PostForm(initial=initial_dict),
    }
    return render(request, 'posts/edit.html', params)


# Takahashi Shunichi
@transaction.atomic
def delete(request, num):
    post = Post.objects.get(id=num)
    if (request.method == 'POST'):
        post.is_deleted = True
        post.save()
        return redirect(to='/posts')

    params = {
        'title': 'ポスト削除',
        'id': num,
        'post': post,
    }
    return render(request, 'posts/delete.html', params)
