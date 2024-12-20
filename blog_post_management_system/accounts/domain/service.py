from accounts.domain.models import UserProfile

class ProfileDomainService:
    """Domain service for profile management"""
    
    @staticmethod
    def get_repo():
        return UserProfile.objects
    
    def get_profile_instance(self,CurrentUser):
        profile, created = self.get_repo().get_or_create(user = CurrentUser)
        return profile