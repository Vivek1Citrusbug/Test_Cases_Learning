from django.test import TestCase
from django.contrib.auth.models import User
from accounts.domain.models import UserProfile


class UserProfileModelTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_create_user_profile(self):
        """
        Creating user profile object
        """
        return UserProfile.objects.create(
            user=self.user, bio="random bio", profile_picture=""
        )

    def test_user_profile_creation(self):
        """
        Testing user profile creation
        """
        user_profile_created = self.test_create_user_profile()
        self.assertTrue(isinstance(user_profile_created, UserProfile))
        self.assertEqual(str(user_profile_created), "testuser's Profile")
        # testing foriegn key relation
        self.assertEqual(user_profile_created.user, self.user)
