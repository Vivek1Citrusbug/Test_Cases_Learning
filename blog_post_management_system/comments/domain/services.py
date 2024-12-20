from comments.domain.models import UserComments

class CommentDomainService:
    """Domain service for comment use cases"""

    @staticmethod
    def get_repo():
        return UserComments.objects

    def list_comments_instance(self,post):
        """Domain services to get comment"""
        return self.get_repo().filter(post_id = post).order_by("-date_posted")

    def delete_comment_instance(self,commentObj,currentUser):
        """Domain service to delete comment"""
        return currentUser == commentObj.user_id or currentUser.is_staff or currentUser == commentObj.post_id.author