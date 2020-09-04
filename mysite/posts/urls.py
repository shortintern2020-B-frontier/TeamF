# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # url(r'', PostView.as_view(), name='index'),
    path('', views.index, name='index')
]
