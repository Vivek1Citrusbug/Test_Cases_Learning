from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
# Create your tests here.

class UserRegistrationTeestCases(TestCase):
    def test_user_registration(self):
        data = {
            'username':'testuser',
            'first_name':'test',
            'last_name':'testlastname',
            'email':'sdsdv@gmail.com',
            'password1':'13novembr200@',
            'password2':'13novembr200@'
        }
        response = self.client.post(reverse('user-registration'),data=data)
        # print(response)
        self.assertEqual(response.status_code,302)    
         
class UserLoginTstcases(TestCase):
    def test_registered_user_login(self):
        data = {
            'username':'vivek',
            'password':'13november200@'
        }
        response = self.client.post(reverse('user-login'),data=data)
        print(response)
        
        self.assertRedirects(response,reverse('blog_list'))
            
