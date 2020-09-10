from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Book, Post, Wokashi, Ahare, Bookmark, Comment, Nice, Category, Tag
from django.contrib.auth.models import User
from .forms import CommentForm, PostForm, TagForm
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
import urllib.parse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from guardian.shortcuts import assign_perm
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse

from collections import defaultdict
import requests
import time
import datetime

# Takahashi Shunichi
RAKUTEN_BOOKS_API_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
RAKUTEN_APP_ID = "1065776451953533134"
NOCOVERPATH = "../static/img/book.png" #表紙がなかった場合に表示する画像のパス
NOITEMURL = "https://books.rakuten.co.jp/search"
def get_book_info(title, author):
    encoded_title = urllib.parse.quote(str(title))
    encoded_author = urllib.parse.quote(str(author))
    response = requests.get("{}?format=json&applicationId={}&title={}&author={}".format(RAKUTEN_BOOKS_API_URL, RAKUTEN_APP_ID, encoded_title, encoded_author))
    cover_path = ''
    if response.status_code != requests.codes.ok:
        cover_path = 'Requests failed'
    elif response.json()["count"] == 0:
        cover_path = NOCOVERPATH
        item_url = NOITEMURL + "?sitem={}".format(title)
    else:
        cover_path = response.json()["Items"][0]["Item"]["largeImageUrl"]
        item_url = response.json()["Items"][0]["Item"]["itemUrl"]
    return cover_path, item_url


def _get_zipped_post(posts, request):
    """Get post related informations.

    Args:
        posts(QuerySet<Post>)

    Author:
        Masato Umakoshi
    """
    wokashi_sum = [
        p.wokashi_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]
    ahare_sum = [
        p.ahare_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]

    books = [Book.objects.get(pk=post.book_id.id) for post in posts]
    bookmark_flag = [
        p.bookmark_set.filter(user_id=request.user.id).exists() for p in posts
    ]
    return zip(posts, wokashi_sum, ahare_sum, books, bookmark_flag)


# Takahashi Shunichi
# Umakoshi Masato
def index(request):
    # TODO Fix naming: book_id.id is too wierd.
    posts = Post.objects.filter(is_deleted=False)

    posts_comments_updated_at = []
    for p in posts:
        is_comment = p.comment_set.exists()
        if is_comment:
            posts_comments_updated_at.append([p, p.comment_set.all().order_by('updated_at').reverse().first().updated_at])
        else:
            posts_comments_updated_at.append([p, p.updated_at])
    sorted_data = sorted(posts_comments_updated_at, key=lambda x: x[1], reverse=True)
    posts = list(map(lambda x: x[0], sorted_data))[:10]

    zipped_post = _get_zipped_post(posts, request)

    params = {
        "title": "ポスト一覧",
        "zipped_post": zipped_post,
    }
    return render(request, "posts/index.html", params)


# Takahashi Shunichi
# Naoki Hirabayashi
def wokashi_create(request, num):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=num)
    try:
        wokashi = Wokashi.objects.get(user_id=user, post_id=post)
        if wokashi.count < 10:
            wokashi.count += 1
    except ObjectDoesNotExist as e:
        wokashi = Wokashi(user_id=user, post_id=post)
    wokashi.save()
    ret_val = post.wokashi_set.all().aggregate(Sum('count'))['count__sum']
    return JsonResponse({'wokashi_sum': ret_val})

    # if request.method == "POST":
    #     user = User.objects.get(id=request.user.id)
    #     post = Post.objects.get(id=request.POST["post_id"])
    #     try:
    #         wokashi = Wokashi.objects.get(user_id=user, post_id=post)
    #         if wokashi.count < 10:
    #             wokashi.count += 1
    #     except ObjectDoesNotExist as e:
    #         wokashi = Wokashi(user_id=user, post_id=post)
    #     wokashi.save()
    #     return redirect(to="/posts")


# Takahashi Shunichi
# Naoki Hirabayashi
def ahare_create(request, num):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=num)
    try:
        ahare = Ahare.objects.get(user_id=user, post_id=post)
        if ahare.count < 10:
            ahare.count += 1
        ret_val = ahare.count
    except ObjectDoesNotExist as e:
        ahare = Ahare(user_id=user, post_id=post)
        ret_val = 1
    ahare.save()
    ret_val = post.ahare_set.all().aggregate(Sum('count'))['count__sum']
    return JsonResponse({'ahare_sum': ret_val})

    # if request.method == "POST":
    #     user = User.objects.get(id=request.user.id)
    #     post = Post.objects.get(id=request.POST["post_id"])
    #     try:
    #         ahare = Ahare.objects.get(user_id=user, post_id=post)
    #         if ahare.count < 10:
    #             ahare.count += 1
    #     except ObjectDoesNotExist as e:
    #         ahare = Ahare(user_id=user, post_id=post)
    #     ahare.save()
    #     return redirect(to="/posts")

#Takahashi Shunichi
def bookmark_create(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=request.POST["post_id"])
        try:
            bookmark = Bookmark.objects.get(user_id=user, post_id=post)
            bookmark.delete()
        except ObjectDoesNotExist as e:
            bookmark = Bookmark(user_id=user, post_id=post)
            bookmark.save()
        return redirect(to="/posts")


# Takahashi Shunichi
# Umakoshi Masato
def detail(request, num):
    post = Post.objects.get(id=num)
    book = Book.objects.get(pk=post.book_id.id)
    comments = Comment.objects.filter(post_id=num)
    user_per_comment = [User.objects.get(pk=comment.user_id.id) for comment in comments]
    num_nices = [
        len(Nice.objects.filter(comment_id=comment.id)) for comment in comments
    ]

    comment_perms = None
    try:
        user = User.objects.get(id=request.user.id)
        if user.is_authenticated:
            comment_perms = [
                user.has_perm('change_delete_content', comment) for comment in comments
            ]
    # When not logged in
    except ObjectDoesNotExist:
        pass

    # When comment_perms is not created.
    if not comment_perms:
        comment_perms = [False for comment in comments]

    zipped_comments = zip(comments, user_per_comment, num_nices, comment_perms)
    params = {
        "title": "ポスト詳細",
        "post": post,
        "book": book,
        "zipped_comments": zipped_comments,
        "form": CommentForm(),
    }
    return render(request, "posts/detail.html", params)


# Takahashi Shunichi
@transaction.atomic
def create(request):
    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        author = request.POST["author"]
        category_id_list = request.POST.getlist('tag')

        try:
            book = Book.objects.get(title=title, author=author)
        except ObjectDoesNotExist as e:
            cover_path, item_url = get_book_info(title, author)
            time.sleep(1)
            book = Book(title=title, author=author, cover_path=cover_path, item_url=item_url)
            book.save()

        user = User.objects.get(id=request.user.id)
        post = Post(user_id=user, content=content, book_id=book)
        post.save()
        if len(category_id_list) != 0:
            for category_id in category_id_list:
                category = Category.objects.get(id=category_id)
                tag = Tag(post_id=post, category_id=category)
                tag.save()
        assign_perm('change_delete_content', user, post)
        return redirect(to="/posts")
    params = {"title": "ポスト投稿", "form": PostForm(), "tag": TagForm()}
    return render(request, "posts/create.html", params)


# Takahashi Shunichi
@transaction.atomic
def edit(request, num):
    post = Post.objects.get(id=num)
    book_id = post.book_id.id
    book = Book.objects.get(id=book_id)
    initial_dict = {
        "content": post.content,
        "title": book.title,
        "author": book.author
    }
    # tag = Tag.objects.filter(post_id=post.id)
    tags = post.tag_set.all()
    category = [tag.category_id.id for tag in tags]

    if request.method == "POST":
        content = request.POST["content"]
        title = request.POST["title"]
        author = request.POST["author"]
        new_category_id_list = request.POST.getlist('tag')
        old_category_id_list = [tag.category_id.id for tag in post.tag_set.all()]

        create_category_id_set = set(new_category_id_list + old_category_id_list) - set(old_category_id_list)
        delete_category_id_set = set(new_category_id_list + old_category_id_list) - set(new_category_id_list)

        user = User.objects.get(id=request.user.id)
        if user.has_perm('change_delete_content', post):
            cover_path, item_url = get_book_info(title, author)
            if Book.objects.filter(title=title, author=author).exists():
                book = Book.objects.filter(title=title, author=author).first()
            else:
                book = Book(title=title, author=author, cover_path=cover_path, item_url=item_url)
                book.save()
            post.content = content
            post.book_id = book
            post.save()
            if len(create_category_id_set) != 0:
                for category_id in create_category_id_set:
                    tag = Tag(post_id=post, category_id=Category.objects.get(id=category_id))
                    tag.save()
            if len(delete_category_id_set) != 0:
                for category_id in delete_category_id_set:
                    tag = Tag.objects.filter(post_id=post, category_id=Category.objects.get(id=category_id))
                    tag.delete()
            return redirect(to="/posts")
        else:
            raise PermissionDenied

    params = {
        "title": "ポスト編集",
        "id": num,
        "form": PostForm(initial=initial_dict),
        "tag": TagForm(initial={'tag':category}),
    }
    return render(request, "posts/edit.html", params)


# Takahashi Shunichi
@transaction.atomic
def delete(request, num):
    post = Post.objects.get(id=num)

    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.has_perm('change_delete_content', post):
            post.is_deleted = True
            post.save()
            return redirect(to="/posts")
        else:
            raise PermissionDenied

    params = {"title": "ポスト削除", "id": num, "post": post}
    return render(request, "posts/delete.html", params)

# Takahashi Shunichi
def bookmark(request):
    bookmark = Bookmark.objects.filter(user_id=request.user.id).all().order_by('updated_at').reverse()
    posts = [
        Post.objects.filter(is_deleted=False).filter(id=b.post_id.id).first() for b in bookmark
    ]
    wokashi_sum = [
        p.wokashi_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]
    ahare_sum = [
        p.ahare_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]
    books = [Book.objects.get(pk=post.book_id.id) for post in posts]
    bookmark_flag = [
        p.bookmark_set.filter(user_id=request.user.id).exists() for p in posts
    ]
    zipped_post = zip(posts, wokashi_sum, ahare_sum, books, bookmark_flag)
    params = {
        "title": "ポスト一覧",
        "zipped_post": zipped_post,
    }
    return render(request, "posts/index.html", params)


# Takahashi Shunichi
def find(request):
    # TODO Fix naming: book_id.id is too wierd.
    post_id_list = []
    category_id_list = []
    if request.method == "POST":
        category_id_list = request.POST.getlist('tag')
        for category_id in category_id_list:
            category = Category.objects.get(id=category_id)
            tags = category.tag_set.all()
            for tag in tags:
                post_id = tag.post_id.id
                post_id_list.append(post_id)
        post_id_set = set(post_id_list)
        posts = Post.objects.filter(is_deleted=False).filter(id__in=post_id_set)
    else:
        posts = Post.objects.filter(is_deleted=False)

    posts_comments_updated_at = []
    for p in posts:
        is_comment = p.comment_set.exists()
        if is_comment:
            posts_comments_updated_at.append([p, p.comment_set.all().order_by('updated_at').reverse().first().updated_at])
        else:
            posts_comments_updated_at.append([p, p.updated_at])
    sorted_data = sorted(posts_comments_updated_at, key=lambda x: x[1], reverse=True)
    posts = list(map(lambda x: x[0], sorted_data))[:10]

    wokashi_sum = [
        p.wokashi_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]
    ahare_sum = [
        p.ahare_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]

    books = [Book.objects.get(pk=post.book_id.id) for post in posts]
    bookmark_flag = [
        p.bookmark_set.filter(user_id=request.user.id).exists() for p in posts
    ]
    zipped_post = zip(posts, wokashi_sum, ahare_sum, books, bookmark_flag)

    params = {
        "title": "ポスト一覧",
        "zipped_post": zipped_post,
        "tag": TagForm(initial={'tag':category_id_list})
    }
    return render(request, "posts/find.html", params)


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
    comment = request.POST["comment"]
    comment = Comment(
        user_id=User.objects.get(pk=user_id),
        post_id=Post.objects.get(pk=num),
        comment=comment,
    )
    comment.save()
    # post_id may be post.id??
    # return HttpResponseRedirect(reverse("posts:show", args=(num, )))
    return redirect(to=f"/posts/{num}")


@transaction.atomic
def comment_edit(request, num):
    """Editting comment function.

    TODO:
        handle
            * Not logged in user
            * Not post request

    Author:
        Masato Umakoshi
    """
    if request.method != "POST":
        raise Http404("Hogehoge")

    comment = Comment.objects.get(id=num)
    content = request.POST["comment"]
    user = User.objects.get(id=request.user.id)
    if user.has_perm('change_delete_content', comment):
        comment.comment = content
        comment.save()
        return redirect(to=f"/posts/{comment.post_id.id}")
    else:
        raise PermissionDenied


@transaction.atomic
def comment_delete(request, num):
    """Deleting comment function.

    TODO:
        handle
            * Not logged in user
            * Not post request

    Author:
        Masato Umakoshi
    """
    if request.method != "POST":
        raise Http404("Hogehoge")

    user = User.objects.get(id=request.user.id)
    comment = Comment.objects.get(id=num)
    if user.has_perm('change_delete_content', comment):
        comment.delete()
        # TODO: redirect to post/id
        return redirect(to=f"/posts/{comment.post_id.id}")
    else:
        raise PermissionDenied


@transaction.atomic
def nice_create(request):
    """Posting nice function.

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
    user = request.user
    comment_id = request.POST["comment_id"]
    comment = Comment.objects.get(pk=comment_id)

    try:
        nice = Nice.objects.get(user_id=user, comment_id=comment)
        nice.delete()
    except ObjectDoesNotExist:
        nice = Nice(
                user_id=user,
                comment_id=comment)
        nice.save()
    return redirect(to=f"/posts/{comment.post_id.id}")


# Naoki Hirabayashi
def load_post_api(request, num):
    # num 番目から (num + 9) 番目の投稿の情報を返す
    posts = Post.objects.filter(is_deleted=False)

    posts_comments_updated_at = []
    for p in posts:
        is_comment = p.comment_set.exists()
        if is_comment:
            posts_comments_updated_at.append([p, p.comment_set.all().order_by('updated_at').reverse().first().updated_at])
        else:
            posts_comments_updated_at.append([p, p.updated_at])
    sorted_data = sorted(posts_comments_updated_at, key=lambda x: x[1], reverse=True)
    posts = list(map(lambda x: x[0], sorted_data))[num:num+10]

    wokashi_sum = [
        p.wokashi_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]
    ahare_sum = [
        p.ahare_set.all().aggregate(Sum('count'))['count__sum'] for p in posts
    ]

    books = [Book.objects.get(pk=post.book_id.id) for post in posts]
    bookmark_flag = [
        p.bookmark_set.filter(user_id=request.user.id).exists() for p in posts
    ]

    jsonDict = {}

    for post in posts:
        elm = {}
        elm['post_id'] = post.id
        elm['post_content'] = post.content
        elm['wokashi_sum'] = post.wokashi_set.all().aggregate(Sum('count'))['count__sum']
        elm['ahare_sum'] = post.ahare_set.all().aggregate(Sum('count'))['count__sum']
        book = Book.objects.get(pk=post.book_id.id)
        elm['book_author'] = book.author
        elm['book_title'] = book.title
        elm['book_cover_path'] = book.cover_path
        elm['bookmark_flag'] = elm['bookmark_flag'] = post.bookmark_set.filter(user_id=request.user.id).exists()
        jsonDict[str(post.id)] = elm

    return JsonResponse(jsonDict)


def ranking(request, kind):
    """Rendering ranking page.

    Args:
        request:
        kind (str):
    """
    kind2class_mapping = {
            'ahare': Ahare,
            'wokashi': Wokashi
    }

    if kind not in kind2class_mapping:
        raise Http404('Please choice ahare or wokashi')
    target_class = kind2class_mapping[kind]
    all_target = target_class.objects.all()
    post_updates = [
            (target.post_id, target.count, target.updated_at)
            for target in all_target]

    # Filtering
    # TODO: This timezone.* should depends on setting
    current_time = datetime.datetime.now(datetime.timezone.utc)
    td = datetime.timedelta(weeks=1)
    valid_posts = [
        (post, count) for post, count, updated_at in post_updates
        if current_time - td <= updated_at
    ]

    # Count and sort posts
    counter = defaultdict(int)
    for post, count in valid_posts:
        counter[post.id] += count
    post_counter_list = [
        (post, counter[post.id]) for post, _ in valid_posts
    ]
    post_counter_list = sorted(post_counter_list, key=lambda x: x[1], reverse=True)[:10]
    sorted_post = [post for post, _ in post_counter_list]
    zipped_post = _get_zipped_post(sorted_post, request)

    params = {
        "zipped_post": zipped_post,
    }

    return render(request, "posts/ranking.html", params)
