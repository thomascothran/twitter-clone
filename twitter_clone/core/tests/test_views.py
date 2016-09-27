from django.test import TestCase, Client
from django.core.urlresolvers import resolve

from ..views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_correct_template_used(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, 'core/homepage.html')
