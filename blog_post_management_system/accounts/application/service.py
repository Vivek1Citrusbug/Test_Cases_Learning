from accounts.domain.service import ProfileDomainService

class ProfileAppService:
    """Application service for profile management"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProfileDomainService()

    def get_profile_application(self,CurrentUser):
        return self.service.get_profile_instance(CurrentUser)