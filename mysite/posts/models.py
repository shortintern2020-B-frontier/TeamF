from django.db import models


# Create your models here.
class Comment(models.Model):
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
