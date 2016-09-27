from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from selenium import webdriver


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}


class EntryCreationTest(LiveServerTestCase):
    """Tests the creation of entries in a user's microblog."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.test_user = User.objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

    def tearDown(self):
        self.browser.quit()
        self.test_user.delete()

    def logUserIn(self, user=None):
        if not User:
            user = self.test_user
        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url + reverse('registration:auth_login').rstrip())
        self.assertIn(
            'login',
            self.browser.current_url
        )
        self.browser.find_element_by_name('username').send_keys(TEST_USER['username'])
        self.browser.find_element_by_id('id_password').send_keys(TEST_USER['password'])
        self.browser.find_element_by_id('submit-login').click()

    def test_whether_user_can_create_an_entry_in_microblog(self):
        test_content = 'SLDFKJEl3kj3ljsdlkfjw'
        self.logUserIn()
        self.browser.get(self.live_server_url + reverse('microblog:create_entry'))
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('microblog:create_entry')
        )
        self.browser.find_element_by_id('id_content').send_keys(test_content)
        self.browser.find_element_by_id('submit-entry')
        self.fail('Finish test!')
