from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Use python manage.py test --keepdb for faster testing. 
# This preserves structure, empties values.

class DashboardTest(TestCase):

    def test_dashboard_view(self):
        self.user = CustomUser.objects.create_user("john", "john@john.com", "securepw123")
        self.client.login(username="john", password="securepw123")

        url = reverse("users:dashboard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cannot_access_dashboard_when_logged_out(self):
        url = reverse("users:dashboard")
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, "users/dashboard.html")
        self.assertRedirects(response, "/login/?next=/dashboard/")


class RegisterTest(TestCase):
    url = reverse("users:register")

    def test_register_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "registration/register.html")
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        response = self.client.post(self.url, data={
            "username": "john",
            "email": "john@john.com",
            "password1": "securepw123",
            "password2": "securepw123",
        })

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertRedirects(response, reverse("users:login"))

def slow_typing(element, text):
   for character in text:
      element.send_keys(character)
      time.sleep(0.3)

# Does the same thing as RegisterTest, but in the browser. Selenium is usually used to check JS/Ajax real-time server behavior.
class RegisterTest2(StaticLiveServerTestCase): #Automatically collects all static files in development. If using LiveServerTestCase, you have to define STATIC_ROOT

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome() #produces broken pipe errors with me, these are harmless, means the test finishes but the proxy is handling a previous request. Firefox() does not.
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_registration(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        
        username = self.selenium.find_element_by_name("username")
        email = self.selenium.find_element_by_name("email")
        password1 = self.selenium.find_element_by_name("password1")
        password2 = self.selenium.find_element_by_name("password2")

        slow_typing(username, 'john')
        slow_typing(email, 'john@john.com')
        slow_typing(password1, 'securepw123')
        slow_typing(password2, 'securepw123')

        self.selenium.find_element_by_name("register").click()

        time.sleep(1)
        assert 'profile was created successfully' in self.selenium.page_source
        self.assertEqual(CustomUser.objects.count(), 1)