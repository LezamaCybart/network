from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.urls import reverse


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('profile', args=(str(self.id)))


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    body = models.TextField()

    likes = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('post-view', args=(str(self.id)))

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="likes_by")
    users = models.ManyToManyField(User, blank=True, null=True, default=None, related_name='liked_by')

    def __str__(self) -> str:
        return f"Like {self.id} to post {self.post} by {self.users}"

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='user')
    following = models.ManyToManyField(User, blank=True, null=True, default=None, related_name='following')
    followers = models.ManyToManyField(User, blank=True, null=True, default=None, related_name='followers')

    def __str__(self) -> str:
        return f"following id: {self.user}, following: {self.following} followers: {self.followers}"
