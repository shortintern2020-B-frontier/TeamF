from django.db import models


# Create your models here.
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
        Masato Umakoshi
    """
    # post = models.ForeignKey(Post)
    # user = models.ForeignKey(User)
    comment = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class FavComment(models.Model):
    # post = models.ForeignKey(Post)
    # user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
