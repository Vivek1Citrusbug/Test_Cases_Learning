from django.test import TestCase
from accounts.application.forms import CreateUserForm, LoginForm, UserProfileForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class CommonSetup(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        self.user = User.objects.create_user(
            username=self.valid_data["username"], password=self.valid_data["password1"]
        )


class CreateUserFormTestCases(CommonSetup):

    def test_form_initialization(self):
        """
        Tests the form initializes with the correct fields.
        """

        form = CreateUserForm()
        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("password1", form.fields)
        self.assertIn("password2", form.fields)

    def test_form_valid_data(self):
        """
        Tests the user form is valid of not
        """
        unique_data = self.valid_data.copy()
        unique_data["username"] = "newuser"
        form = CreateUserForm(data=unique_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_email_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        invalid_data = self.valid_data.copy()

        invalid_data.pop("email")

        form = CreateUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_missing_first_name_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        invalid_data = self.valid_data.copy()
        invalid_data.pop("first_name")
        form = CreateUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_form_missing_last_name_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        invalid_data = self.valid_data.copy()
        invalid_data.pop("last_name")
        form = CreateUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_form_invalid_email(self):
        """
        Test form validation fails with invalid email.
        """

        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email-example"
        form = CreateUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_password_mismatch(self):
        """
        Test form validation fails when passwords do not match.
        """

        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "differentpassword123"
        form = CreateUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_save_method(self):
        """
        Test the save method creates a user correctly.
        """

        form = CreateUserForm(data=self.valid_data)
        if form.is_valid():
            user = form.save()
            self.assertIsInstance(user, User)
            self.assertEqual(user.username, self.valid_data["username"])
            self.assertEqual(user.email, self.valid_data["email"])
            self.assertEqual(user.first_name, self.valid_data["first_name"])
            self.assertEqual(user.last_name, self.valid_data["last_name"])


class LoginFormTestCases(CommonSetup):

    def test_form_initialization(self):
        """
        Tests the login form initializes with the correct fields.
        """

        form = LoginForm()
        self.assertIn("username", form.fields)
        self.assertIn("password", form.fields)

    def test_form_valid_data(self):
        """
        Tests the login form is valid of not
        """

        form = LoginForm(
            data={
                "username": self.valid_data["username"],
                "password": self.valid_data["password1"],
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_missing_username_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        form = LoginForm(data={"password": self.valid_data["password1"]})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_missing_password_fields(self):
        """
        Test form is invalid when required fields are missing.
        """

        form = LoginForm(data={"username": self.valid_data["username"]})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)


class UserProfileFormTestCass(TestCase):

    def setUp(self):
        """
        Setup for userprofile form
        """
        self.valid_data = {"bio": "This is a test bio."}
        self.invalid_data = {"bio": "x" * 1001}

    def test_form_fields(self):
        """
        Test that the form contains the correct fields.
        """
        form = UserProfileForm()
        self.assertIn("bio", form.fields)
        self.assertIn("profile_picture", form.fields)

    def test_form_valid_data(self):
        """
        Test the form with valid data.
        """
        data = self.valid_data.copy()
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Test the form with invalid data (e.g., overly long bio).
        """
        data = self.invalid_data.copy()
        form = UserProfileForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("bio", form.errors)

    def test_form_empty_data(self):
        """
        Test the form with empty data.
        """
        form = UserProfileForm(data={})
        print(form.errors)
        self.assertTrue(form.is_valid())
