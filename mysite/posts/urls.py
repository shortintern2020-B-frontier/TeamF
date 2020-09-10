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
#     path("find", views.find, name="find"),
]
