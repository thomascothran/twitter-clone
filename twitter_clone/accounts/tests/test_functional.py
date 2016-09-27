from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver

# Create your tests here.

class AccountRegistrationTest(LiveServerTestCase):
    """Tests the experience of a prospective new user, Jerry."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # Jerry, a new user, navigates to the home page
    def test_sign_up_process(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('signup-button').click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('accounts:signup')
        )
