from django.contrib import admin
from .models import User, Book, Post, Wokashi, Ahare, Bookmark, Comment, Nice

# Takahashi Shunichi
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Post)
admin.site.register(Wokashi)
admin.site.register(Ahare)
admin.site.register(Bookmark)
admin.site.register(Comment)
admin.site.register(Nice)
