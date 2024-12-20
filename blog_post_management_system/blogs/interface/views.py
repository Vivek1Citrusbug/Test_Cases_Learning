from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..application.forms import BlogPostForm
from blogs.application.services import BlogPostAppService
from blogs.domain.models import BlogPost


class BlogPostListingView(LoginRequiredMixin, ListView):
    """Handles listing all posts"""

    template_name = "blogs/blog_list.html"
    context_object_name = "posts"
    model: BlogPost
    ordering = ["-date_published"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BlogPostAppService()

    def get_queryset(self):
        return self.service.list_posts_application()


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Handles listing specific post"""

    template_name = "blogs/blog_detail.html"
    context_object_name = "post"
    model: BlogPost

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BlogPostAppService()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["likes_count"] = post.likes.count()
        context["user_liked"] = post.likes.filter(user=self.request.user).exists()
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        if not pk:
            raise Http404("Post not found.")
        return self.service.get_post_details_application(pk)


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new blog post."""

    form_class = BlogPostForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")
    model: BlogPost
    context_object_name = "post"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BlogPostAppService()

    def form_valid(self, form):
        print("Current requesting user : ", self.request.user)
        self.service.create_post_application(
            title=form.cleaned_data["title"],
            content=form.cleaned_data["content"],
            author=self.request.user,
        )
        return HttpResponseRedirect(self.success_url)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Handles updating an existing blog post."""

    form_class = BlogPostForm
    template_name = "blogs/blog_form.html"
    success_url = reverse_lazy("blog_list")
    model: BlogPost
    context_object_name = "post"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BlogPostAppService()

    def get_object(self, queryset=None):
        return self.service.get_post_details_application(self.kwargs["pk"])

    def test_func(self):
        blog = self.service.get_post_details_application(self.kwargs["pk"])
        return blog.author == self.request.user


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Handles deleting a blog post."""

    template_name = "blogs/blog_confirm_delete.html"
    success_url = reverse_lazy("blog_list")
    model: BlogPost
    context_object_name = "post"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BlogPostAppService()

    def get_object(self, queryset=None):
        return self.service.get_post_details_application(self.kwargs["pk"])

    def test_func(self):
        blog = self.service.get_post_details_application(self.kwargs["pk"])
        return blog.author == self.request.user or self.request.user.is_staff

