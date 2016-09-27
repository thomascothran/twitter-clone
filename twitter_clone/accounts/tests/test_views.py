from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class SignupViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_whether_url_resolves_to_view(self):
        client = Client()
        response = client.get(reverse('accounts:signup'))