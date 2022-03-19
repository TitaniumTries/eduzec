from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

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
