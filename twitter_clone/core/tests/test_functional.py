from django.test import TestCase
from django.test import LiveServerTestCase

from selenium import webdriver

# Create your tests here.

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
