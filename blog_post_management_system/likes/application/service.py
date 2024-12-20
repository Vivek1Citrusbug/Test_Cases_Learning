from likes.domain.service import LikeDomainService

class LikeApplicationService:
    def __init__(self):
        """Initialize domain service"""
        self.service = LikeDomainService()
        
    def like_application(self,post,user):
        return self.service.like_instance(post,user)