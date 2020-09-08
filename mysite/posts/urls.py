# from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:num>", views.detail, name="detail"),
    path("delete/<int:num>", views.delete, name="delete"),
    path("create", views.create, name="create"),
    path("edit/<int:num>", views.edit, name="edit"),
    path("hoge/<int:num>", views.comment_create, name="hoge"),
    path("nice", views.nice_create, name="nice"),
    path("wokashi", views.wokashi_create, name="wokashi"),
    path("ahare", views.ahare_create, name="ahare"),
    path("bookmark", views.bookmark_create, name='bookmark'),
    path("comment_edit/<int:num>", views.comment_edit, name="comment_edit"),
    path("comment_delete/<int:num>",
         views.comment_delete,
         name="comment_delete"),
]
