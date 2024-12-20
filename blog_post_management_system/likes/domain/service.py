from django.shortcuts import redirect
from likes.domain.models import Like

class LikeDomainService:
    @staticmethod
    def get_repo():
        return Like.objects
    
    def like_instance(self,post,user):
        like, created = self.get_repo().get_or_create(post=post, user=user)

        if not created:
            like.delete()

        return redirect("blog_detail", pk=post.pk)