
from django.urls import path

from . import views
from .views import NewPost, Post, AllPostsView, ProfileView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("post/<int:pk>", views.PostView.as_view(), name="post-view"),
    path("all-posts", views.AllPostsView.as_view(), name="all-posts"),

    path("new_post", views.NewPost.as_view(), name="new-post"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile")
]
