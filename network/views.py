from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

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

class PostView(DetailView):
    model = Post
    template_name = 'network/post.html'
    context_object_name = 'post'

    """
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
    """

class AllPostsView(ListView):
    model = Post
    template_name = 'network/all-posts.html'

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    """
