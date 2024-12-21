from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from accounts.domain.models import UserProfile

# Create your tests here.


class UserRegistrationTestCases(TestCase):

    def setUp(self):
        """
        Common setup for user registration tests.
        """

        self.valid_data = {
            "username": "testuser",
            "first_name": "test",
            "last_name": "testlastname",
            "email": "sdsdv@gmail.com",
            "password1": "13novembr200@",
            "password2": "13novembr200@",
        }
        self.invalid_data = {
            "username": "",
            "password1": "123",
            "password2": "12dcsdc3",
            "email": "invalidemail",
        }

    def test_user_registration(self):
        """
        User registration testing
        """

        response = self.client.post(reverse("user-registration"), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "sdsdv@gmail.com")
        self.assertRedirects(response, reverse("user-login"))

    def test_user_registration_invalid_data(self):
        """
        Test user registration with invalid data
        this function will work for any typ of user registration form error.
        """

        response = self.client.post(
            reverse("user-registration"), data=self.invalid_data
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)


class UserLoginTestcases(TestCase):

    def setUp(self):
        """
        Create a user for testing login functionality
        """

        self.credentials = {"username": "testuser", "password": "secretpassword"}
        self.user = User.objects.create_user(**self.credentials)

    def test_registered_user_login(self):
        """
        Test login with valid credentials
        """

        response = self.client.post(reverse("user-login"), self.credentials)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse("blog_list"))

    def test_invalid_user_login(self):
        """
        Test login with invalid credentials, for any type of login form error this function will test for it.
        """

        invalid_credentials = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post(reverse("user-login"), invalid_credentials)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserLogoutTestCases(TestCase):

    def setUp(self):
        """
        Set up a test user and log them in
        """

        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_logout_redirect(self):
        """
        Test if logout redirects to the home page
        """

        response = self.client.get(reverse("user-logout"))
        self.assertRedirects(response, reverse("home_page"))


class UserProfileDetailTestCases(TestCase):

    def setUp(self):
        """
        Setup for user profile detail view
        """

        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = UserProfile.objects.create(user=self.user, bio="Test Bio")
        self.url = reverse("profile")

    def test_redirect_if_not_logged_in(self):
        """
        If not logged in then user will be redirected to login page
        """

        response = self.client.get(self.url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_view_with_logged_in_user_get_request(self):
        """
        If logged in then user will be redirected to edit profile form
        """

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class UserProfileUpdateTestCases(TestCase):

    def setUp(self):
        """
        Setup for user profile updatation.
        """

        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = UserProfile.objects.create(user=self.user)
        self.url = reverse("profile_edit")
        self.data = {"bio": "", "profil_picture": ""}

    def test_redirect_if_not_logged_in(self):
        """
        If not logged in then user will be redirected to login page
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        print(response.url)
        self.assertIn("login", response.url)

    def test_view_with_logged_in_user_get_request(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        print(response.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("edit", response.url)

    def test_successful_post_request(self):
        """
        If logged in then user will be redirected to profile page after successfully updating profile
        """

        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
