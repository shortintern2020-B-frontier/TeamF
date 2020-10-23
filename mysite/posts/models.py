from django.db import models
from django.contrib.auth.models import User

# Takahashi Shunichi
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_path = models.CharField(max_length=255)
    item_url = models.CharField(max_length=255, default='https://books.rakuten.co.jp/')

    class Meta:
        unique_together = ('title', 'author')


# Takahashi Shunichi
class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('change_delete_content', 'Change Delete content'),
        )


# Takahashi Shunichi
class Wokashi(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'post_id')


# Takahashi Shunichi
class Ahare(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'post_id')


# Takahashi Shunichi
class Bookmark(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'post_id')


class Comment(models.Model):
    """Comment model for comment on threads.

    Scheme:
        comment: varchar(500)
        created_at: timestamp
        updated_at: timestamp
        is_deleted: bool

    Note:
        is_deleted is `True` means that the comment is deleted.

    Author:
        Takahashi Shunichi
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('change_delete_comment', 'Change Delete comment'),
        )

    def __str__(self):
        return self.comment


# Takahashi Shunichi
class Nice(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'comment_id')


# Takahashi Shunichi
class Category(models.Model):
    category = models.CharField(max_length=255)


# Takahashi Shunichi
class Tag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id =  models.ForeignKey(Category, on_delete=models.CASCADE)


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, default=0)
    review = models.CharField(max_length=500)
    title = models.CharField(max_length=255, default="none")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)