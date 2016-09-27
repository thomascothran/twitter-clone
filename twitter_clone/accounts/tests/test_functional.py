from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from selenium import webdriver


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}

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
