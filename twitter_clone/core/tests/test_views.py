from django.test import Client, TransactionTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth import get_user_model

from ..views import home_page
from microblog.models import Entry

TEST_USER = {
    'username': 'username2342lskejr3',
    'email': 'emailadd@email.com',
    'password': 'alsdjf2343**YH'
}
TEST_USER2 = {
    'username': 'skejr3wekrjwl',
    'email': 'email3423@email.com',
    'password': 'alsdjf2343**YH'
}
TEST_USER3 = {
    'username': 'wekr4293',
    'email': 'email23403@email.com',
    'password': 'alsdjf2343**YH'
}
TEST_POSTS = {
    'users_own_post': 'asldfje2o3ij',
    'user_being_followed_post': 'as3oiofjwokd',
    'user_not_being_followed_post': 'nswkjjliosdfj'
}


class HomePageTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_user2 = get_user_model().objects.create_user(
            TEST_USER2['username'], TEST_USER2['email'], TEST_USER2['password']
        )
        self.test_user3 = get_user_model().objects.create_user(
            TEST_USER3['username'], TEST_USER3['email'], TEST_USER3['password']
        )
        self.test_own_post = Entry.objects.create(
            content=TEST_POSTS['users_own_post'],
            creator=self.test_user
        )
        self.test_followers_post = Entry.objects.create(
            content=TEST_POSTS['user_being_followed_post'],
            creator=self.test_user2
        )
        self.test_nonfollowers_post = Entry.objects.create(
            content=TEST_POSTS['user_not_being_followed_post'],
            creator=self.test_user3
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

    def test_that_user_sees_own_posts_on_homepage(self):
        client = Client()
        client.force_login(self.test_user)
        response = client.get('/')
        self.assertContains(
            response,
            self.test_own_post.content
        )

    def test_that_user_sees_user_shes_followings_posts_on_homepage(self):
        client = Client()
        client.force_login(self.test_user)
        self.test_user.userprofile.following.add(
            self.test_user2.userprofile
        )
        response = client.get('/')
        self.assertContains(
            response,
            self.test_followers_post.content
        )

    def test_that_user_sees_user_shes_followings_posts_on_homepage(self):
        client = Client()
        client.force_login(self.test_user)
        self.test_user.userprofile.following.add(
            self.test_user2.userprofile
        )
        response = client.get('/')
        self.assertContains(
            response,
            self.test_followers_post.content
        )

    def test_that_user_does_not_see_nonfollwer_posts_on_homepage(self):
        client = Client()
        client.force_login(self.test_user)
        response = client.get('/')
        self.assertNotContains(
            response,
            self.test_nonfollowers_post.content
        )
