import json
from django.http import JsonResponse
from braces.views import CsrfExemptMixin
from network.utils import does_like, is_following
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Following, Likes, User, Post

class PostForm(forms.Form):
    body = forms.Textarea()

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

class NewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'network/new-post.html'
    fields = ('body',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.likes = 0
        form.instance.date
        return super().form_valid(form)

class PostView(CsrfExemptMixin, DetailView):
    model = Post
    template_name = 'network/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['user_id'] = self.request.user.id
            context['like_count'] = Likes.objects.get_or_create(post=kwargs['object'])[0].users.all().count()
            context['does_like'] = does_like(self.request.user.id, kwargs['object'].id)

            return context
    
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)

        post_id = data.get("post_id")
        post = Post.objects.get(id=post_id)

        if data.get("like") == True:
            like = Likes.objects.get(post=post)
            user = User.objects.get(id=data.get("user_id"))
            if does_like(user.id, post.id):
                like.users.remove(user)
                like.save()
                return JsonResponse({"message": "unliked"}, status=200)
            else:
                like.users.add(user)
                like.save()
                return JsonResponse({"message": "liked"}, status=200)

        new_body = data.get("new_body")

        post.body = new_body
        post.save()
        return JsonResponse({"message": "saved"}, status=201)



class AllPostsView(ListView):
    model = Post
    template_name = 'network/all-posts.html'
    paginate_by = 10

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    """

class FollowingView(ListView):
    model = Post
    template_name = 'network/following-posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = Following.objects.get(user=self.request.user).following.all()
        posts = Post.objects.all()

        following_posts = list()

        for post in posts:
            author = post.author
            if author in following:
                following_posts.append(post)
    
        context['posts'] = following_posts

        return context

class ProfileView(CsrfExemptMixin, DetailView):
    model = User
    template_name = 'network/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Following.objects.get_or_create(user=kwargs['object'])[0]
        profile_user = User.objects.get(id=kwargs['object'].id)

        context['profile_user_id'] = profile_user.id
        context['user_id'] = self.request.user.id

        context['followers'] = profile.followers.all().count()
        context['following'] = profile.following.all().count()
        context['is_following'] = is_following(self.request.user, profile.user)
        return context
    
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = data.get("user")
        profile = data.get("profile")

        user_f = Following.objects.get_or_create(id=user)[0]
        profile_f = Following.objects.get_or_create(id=profile)[0]

        profile_user_followers = profile_f.followers
        user_following = user_f.following

        if is_following(user, profile):
            profile_user_followers.remove(user_f.user)
            user_following.remove(profile_f.user)

            user_f.save()
            profile_f.save()
            return JsonResponse({"message": "unfollow"}, status=200)

        else:
            profile_user_followers.add(user_f.user)
            user_following.add(profile_f.user)

            user_f.save()
            profile_f.save()
            return JsonResponse({"message": "follow"}, status=201)

