from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from selenium import webdriver
from microblog.models import Entry

# Create your tests here.

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

class NewVisitorTest(LiveServerTestCase):
    """Tests the experience of a prospective new user, Jerry."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # Jerry, a new user, navigates to the home page
    def test_whether_new_user_sees_welcome_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Twitter", self.browser.title)

    # Jerry sees a sign in button
    def test_whether_sign_in_button_shows_up_for_logged_out_user(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("signin-button").click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/accounts/login/'
        )

        # Jerry realizes he doesn't have an account, and goes back to the homepage
        self.browser.find_element_by_id('homepage-icon').click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/'
        )

        # Jerry clicks on the sign up button
        self.browser.find_element_by_id('signup-button').click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/accounts/register/'
        )

class LoggedInUserTest(LiveServerTestCase):
    """This tests the way the base template should look to a logged in user."""
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

    def tearDown(self):
        self.browser.quit()


class FeedTest(LiveServerTestCase):
    """This tests the feed to ensure users see their own posts and those they follow"""
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
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

    def tearDown(self):
        self.browser.quit()

    def logUserIn(self):
        """This is a helper function to log a user in with the selenium browser."""
        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url + reverse('registration:auth_login').rstrip())
        self.assertIn(
            'login',
            self.browser.current_url
        )
        self.browser.find_element_by_name('username').send_keys(TEST_USER['username'])
        self.browser.find_element_by_id('id_password').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('submit-login').click()

    def test_whether_correct_posts_show_up_in_feed(self):
        self.logUserIn()
        self.test_user.userprofile.following.add(
            self.test_user2.userprofile
        )
        self.browser.get(
            self.live_server_url + '/',
        )
        self.assertIn(
            self.test_own_post.content,
            self.browser.page_source
        )
        self.assertIn(
            self.test_followers_post.content,
            self.browser.page_source
        )
        self.assertNotIn(
            self.test_nonfollowers_post.content,
            self.browser.page_source
        )
