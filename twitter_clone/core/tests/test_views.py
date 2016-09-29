from django.test import Client, TransactionTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth import get_user_model

from ..views import home_page

TEST_USER = {
    'username': 'username2342lskejr3',
    'email': 'emailadd@email.com',
    'password': 'alsdjf2343**YH'
}


class HomePageTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_correct_template_used(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, 'core/homepage.html')

    def test_that_logged_user_sees_certain_navbar_buttons(self):
        client = Client()
        client.force_login(self.test_user)
        response = client.get('/')
        self.assertContains(
            response,
            reverse('microblog:user_profile', kwargs={'pk': self.test_user.pk})
        )
        self.assertContains(
            response,
            reverse('microblog:user_list')
        )
        self.assertContains(
            response,
            reverse('microblog:create_entry')
        )
        self.assertNotContains(
            response,
            '/accounts/login'
        )
        self.assertNotContains(
            response,
            '/accounts/register'
        )


    def test_that_logged_out_user_does_not_see_certain_navbar_buttons(self):
        client = Client()
        response = client.get('/')
        self.assertNotContains(
            response,
            reverse('microblog:user_profile', kwargs={'pk': self.test_user.pk})
        )
        self.assertNotContains(
            response,
            reverse('microblog:user_list')
        )
        self.assertNotContains(
            response,
            reverse('microblog:create_entry')
        )
        self.assertContains(
            response,
            '/accounts/login'
        )
        self.assertContains(
            response,
            '/accounts/register'
        )
