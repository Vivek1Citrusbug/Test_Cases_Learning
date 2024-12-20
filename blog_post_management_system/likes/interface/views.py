from django.shortcuts import render
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from blogs.domain.models import BlogPost
from django.views.generic import DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from likes.domain.models import Like
from blogs.application.services import BlogPostAppService
from likes.application.service import LikeApplicationService
# Create your views here.


@method_decorator(login_required, name="dispatch")
class LikeView(View):
    """This view is used to like user blogs"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.PostsService = BlogPostAppService()
        self.LikeService = LikeApplicationService()

    def post(self, request, *args, **kwargs):
        post = self.PostsService.get_post_details_application(self.kwargs["pk"])
        user = request.user
        return self.LikeService.like_application(post,user)
        