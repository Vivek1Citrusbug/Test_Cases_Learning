from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from comments.domain.models import UserComments
from blogs.domain.models import BlogPost
from comments.application.forms import CommentForm
from django.shortcuts import get_object_or_404
from blogs.application.services import BlogPostAppService
from comments.application.services import CommentAppService


class CommentListView(LoginRequiredMixin, ListView):
    """This view is used to list user comments"""

    model = UserComments
    template_name = "comments/list_comments.html"
    context_object_name = "comments"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.PostsService = BlogPostAppService()
        self.CommentService = CommentAppService()

    def get_queryset(self):
        post = self.PostsService.get_post_details_application(post_id=self.kwargs["pk"])
        print("post printed : ", post.content, post.date_published, post.author)
        return self.CommentService.get_comments_application(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.PostsService.get_post_details_application(
            post_id=self.kwargs["pk"]
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """This view is used to create new user comments"""

    model = UserComments
    template_name = "comments/create_comment.html"
    form_class = CommentForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.PostsService = BlogPostAppService()
        self.CommentService = CommentAppService()

    def form_valid(self, form):
        post = self.PostsService.get_post_details_application(post_id=self.kwargs["pk"])
        form.instance.user_id = self.request.user
        form.instance.post_id = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_comment", kwargs={"pk": self.kwargs["pk"]})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """This view is used to delete user comments"""

    model = UserComments
    template_name = "comments/delete_comment.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.PostsService = BlogPostAppService()
        self.CommentService = CommentAppService()

    def get_success_url(self):
        return reverse_lazy("list_comment", kwargs={"pk": self.object.post_id.pk})

    def test_func(self):
        """
        Ensure only the comment's author or admin can delete the comment.
        """
        comment = self.get_object()
        return self.CommentService.delete_comment_application(
            comment, self.request.user
        )
