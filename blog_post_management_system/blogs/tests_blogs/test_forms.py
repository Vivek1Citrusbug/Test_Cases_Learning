from django import forms
from django.test import TestCase
from blogs.domain.models import BlogPost
from django.core.exceptions import ValidationError
from blogs.application.forms import BlogPostForm
from django.contrib.auth.models import User

class BlogPostFormTestCases(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "test title",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        }
        self.user = User.objects.create_user(username='username',password='password')

    def test_form_initialization(self):
        """
        Tests the form initializes with the correct fields.
        """

        form = BlogPostForm()
        self.assertIn("title", form.fields)
        self.assertIn("content", form.fields)

    def test_form_valid_data(self):
        """
        Tests the user form is valid of not
        """

        form = BlogPostForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_title_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        invalid_data = self.valid_data.copy()

        invalid_data.pop("title")

        form = BlogPostForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_missing_content_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        invalid_data = self.valid_data.copy()
        invalid_data.pop("content")
        form = BlogPostForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_form_content_length_fields(self):
        """
        Test form is invalid when required fields are less than length.
        """

        invalid_data = self.valid_data.copy()
        invalid_data['content'] = 'sdfvsdv'
        form = BlogPostForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


    def test_save_method(self):
        """
        Test the save method creates a blog correctly.
        """

        form = BlogPostForm(data=self.valid_data)
        if form.is_valid():
            form.instance.author = self.user
            blog = form.save()
            self.assertIsInstance(blog, BlogPost)
            self.assertEqual(blog.author, self.user)
            self.assertEqual(blog.title, self.valid_data["title"])
            self.assertEqual(blog.content, self.valid_data["content"])
           

    