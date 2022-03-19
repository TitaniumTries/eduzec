from django.test import TestCase
from django.urls import reverse

class LandingPageTest(TestCase):

    def test_landing_page_uses_index_template(self):
        url = reverse("landing")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "index.html")