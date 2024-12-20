from comments.domain.services import CommentDomainService

class CommentAppService:
    def __init__(self):
        """Initialize domain service"""
        self.service = CommentDomainService()

    def get_comments_application(self,post):
        """Application service to get comments by post id"""
        return self.service.list_comments_instance(post)

    def delete_comment_application(self,commentObj,currentUserObj):
        """Application Service to delete comments"""
        return self.service.delete_comment_instance(commentObj,currentUserObj)