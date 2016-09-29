from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

from selenium import webdriver

# Create your tests here.

TEST_USER = {
    'username': 'username2342lskejr3',
    'email': 'emailadd@email.com',
    'password': 'alsdjf2343**YH'
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
        self.browser.find_element_by_xpath("//nav//a[text()='Sign In']").click()
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
        try:
            self.browser.find_element_by_xpath("//nav//a[text()='Sign Up']").click()
        except:
            self.browser.maximize_window()
            self.browser.find_element_by_xpath("//nav//a[text()='Sign Up']").click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + 'accounts/register'
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

