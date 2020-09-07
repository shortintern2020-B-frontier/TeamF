# from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:num>', views.detail, name='detail'),
    path('<int:num>/delete', views.delete, name='delete'),
    path('create', views.create, name='create'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('comment_create/<int:num>', views.edit, name='comment_create'),
]
