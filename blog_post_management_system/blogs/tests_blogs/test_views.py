from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from blogs.domain.models import BlogPost
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class BaseSetupClass(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.url = reverse("blog_list")
        
        self.post1 = BlogPost.objects.create(
            title="Post 1",
            content="Content of post 1",
            author=self.user,
            date_published=datetime.now() - timedelta(days=1)
        )

        self.post2 = BlogPost.objects.create(
            title="Post 2",
            content="Content of post 2",
            author=self.user,
            date_published=datetime.now()
        )

class BlogPostListingViewTestCases(BaseSetupClass):

    def test_login_required(self):
        """
        Test that the view requires login.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn(reverse("user-login"), response.url)
    
    def test_view_renders_template(self):
        """
        Test that the view renders the correct template for logged-in users.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blog_list.html")

    def test_view_queryset(self):
        """
        Test that the view returns the correct queryset.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        posts = response.context["posts"]
        self.assertEqual(list(posts), [self.post1,self.post2])


class BlogDetailViewTestCases(BaseSetupClass):

    def setUp(self):
        super().setUp()
        self.url = reverse("blog_detail", kwargs={"pk": self.post1.pk})

    def test_access_without_login(self):
        """Test that the view redirects to login if user is not authenticated"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  
        self.assertIn(reverse("user-login"), response.url)

    def test_access_with_login(self):
        """Test that the view renders successfully for authenticated users"""

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogs/blog_detail.html")
        self.assertEqual(response.context["post"], self.post1)

    def test_context_data(self):
        """Test that the context data contains likes_count and user_liked"""

        self.post1.likes_count.add(self.user)
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("blog_detail", kwargs={"pk": self.post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["likes_count"], 1) 
        self.assertTrue(response.context["user_liked"])

    def test_get_object_valid_pk(self):
        """Test that get_object fetches the correct blog post"""

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.context["post"], self.post1)

    def test_get_object_invalid_pk(self):
        """Test that get_object raises 404 for an invalid pk"""

        self.client.login(username="testuser", password="testpassword")
        invalid_url = reverse("blog_detail", kwargs={"pk": 999})  
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

