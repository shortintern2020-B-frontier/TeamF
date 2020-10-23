# from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:num>", views.detail, name="detail"),
    path("delete/<int:num>", views.delete, name="delete"),
    path("create", views.create, name="create"),
    path("edit/<int:num>", views.edit, name="edit"),
    path("comment_create/<int:num>", views.comment_create, name="comment_create"),
    path("nice", views.nice_create, name="nice"),
    path("wokashi/<int:num>", views.wokashi_create, name="wokashi"),
    path("ahare/<int:num>", views.ahare_create, name="ahare"),
    path("bookmark", views.bookmark_create, name='bookmark'),
    path("comment_edit/<int:num>", views.comment_edit, name="comment_edit"),
    path("comment_delete/<int:num>",
         views.comment_delete,
         name="comment_delete"),
    path("fuga", views.bookmark, name="fuga"),
    path("load_post_api/<int:num>", views.load_post_api, name="post_api"),
    path("fuga", views.bookmark, name="fuga"),
    path("find", views.find, name="find"),
    # Ranking
    path("ranking/<str:kind>", views.ranking, name="ranking"),
    # PostList
    path("postList", views.postList, name="postList"),
    # Review
    path("review_edit/<int:num>", views.review_edit, name="review_edit"),
    path("review_create/<int:num>", views.review_create, name="review_create"),
    path("review_book_select", views.review_book_select, name="review_book_select"),
    path("review/<int:num>", views.review, name="review"),
]
