from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from selenium import webdriver


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}
TEST_USER2 = {
    'username': 'eljw',
    'password': 'sweaj21a3*)(#J',
    'email': 'ae@gmail.com',
}

# Helper functions

def selenium_login(browser, username, password, login_url):
    """This is a helper function to log a user in with the selenium browser."""
    browser.get(login_url)
    browser.find_element_by_name('username').send_keys(username)
    browser.find_element_by_id('id_password').send_keys(password)
    browser.find_element_by_id('submit-login').click()

# Create your tests here.

class AccountRegistrationTest(LiveServerTestCase):
    """Tests the experience of a prospective new user, Jerry."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_sign_up_process(self):
        # Jerry, a new user, navigates to the home page
        self.browser.get(self.live_server_url)
        # Seeing the invitation to sign up, he clicks the signup up buttn
        self.browser.find_element_by_id('signup-button').click()
        # He is sent to the registration page, where he filles out the form
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/accounts/register/'
        )
        self.browser.find_element_by_id('id_username').send_keys(TEST_USER['username'])
        self.browser.find_element_by_id('id_email').send_keys(TEST_USER['email'])
        self.browser.find_element_by_id('id_password1').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('id_password2').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('submit-registration').click()
        # Let's make sure a user was in fact created.
        self.assertEqual(
            TEST_USER['username'],
            get_user_model().objects.get(username=TEST_USER['username']).username
        )
        # Jerry is redirected to the home page.
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/'
        )

class LoginTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('signin-button').click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/accounts/login/'
        )

        self.browser.find_element_by_name('username').send_keys(TEST_USER['username'])
        self.browser.find_element_by_id('id_password').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('submit-login').click()
        # Check that we redirect to home page
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/'
        )


class TestFollowers(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_user2 = get_user_model().objects.create_user(
            TEST_USER2['username'], TEST_USER2['email'], TEST_USER2['password']
        )

    def tearDown(self):
        self.browser.quit()

    def log_user_in(self, user_dict=TEST_USER):
        self.browser.get(self.live_server_url + '/accounts/login')
        self.browser.find_element_by_name('username').send_keys(TEST_USER['username'])
        self.browser.find_element_by_id('id_password').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('submit-login').click()

    def test_whether_one_user_can_follow_another(self):
        # Jenny wants to follow Jerry.
        # First, she logs in
        self.log_user_in()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + '/'
        )
        # Then she goes to Jerry's profile page
        self.browser.get(
            self.live_server_url +
            reverse('microblog:user_profile', kwargs={'pk': self.test_user2.pk})
        )
        self.assertEqual(
            self.browser.current_url,
            (self.live_server_url +
             reverse('microblog:user_profile', kwargs={'pk': self.test_user2.pk}))
        )
        # She clicks the link to follow him
        self.browser.find_element_by_id(
            'follow-u-{}'.format(self.test_user2.pk)
        ).click()
        # Check that we were correctly redirected
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('microblog:user_profile',
                                           kwargs={'pk': self.test_user2.pk})
        )
        self.assertIn(
            self.test_user2.userprofile,
            self.test_user.userprofile.following.all()
        )
        # She then goes to the user list
        self.browser.get(
            self.live_server_url +
            reverse('microblog:user_list')
        )
        # She sees a button that says "following"
        # She clicks it to unfollow him
