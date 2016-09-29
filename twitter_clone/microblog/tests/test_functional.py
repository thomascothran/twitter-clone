from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from selenium import webdriver

from .. import models

TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}

TEST_USER2 = {
    'username': 'asdfl12io',
    'password': 'sarjla3*fk(#J',
    'email': 'klilhsfls@gmail.com',
}

class EntryCreationTest(LiveServerTestCase):
    """Tests the creation of entries in a user's microblog."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(6)
        self.test_user = User.objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_user2 = User.objects.create_user(
            TEST_USER2['username'], TEST_USER2['email'], TEST_USER2['password']
        )
        self.test_tweet = models.Entry.objects.create(
            content="sfalekrjo3ijsdfklsj3oi32",
            creator=self.test_user,
        )

    def tearDown(self):
        self.browser.quit()
        self.test_user.delete()

    def logUserIn(self, user=None):
        """This is a helper function to log a user in with the selenium browser."""
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
        """Jerry, a current user, decides he wants to post an entry"""
        test_content = 'SLDFKJEl3kj3ljsdlkfjw'
        # Jerry logs in
        self.logUserIn()
        # Jerry navigates to the create entry page
        self.browser.get(self.live_server_url + reverse('microblog:create_entry'))
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('microblog:create_entry')
        )
        # Jerry fills out the form
        self.browser.find_element_by_id('id_content').send_keys(test_content)
        self.browser.find_element_by_id('submit-entry').click()
        # Check that entry was created
        test_entry = models.Entry.objects.get(content=test_content)
        self.assertEqual(
            test_content,
            test_entry.content,
        )
        # Check that user was redirected to detail page
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('microblog:entry_detail', kwargs={'pk': test_entry.pk})
        )
        # Jerry looks for his microblog to review his work.
        self.assertIn(
            test_entry.content,
            self.browser.page_source
        )

    def test_whether_user_can_see_other_users_entries(self):
        """Jenni, a present user, decides to view a friends blog entries."""
        self.logUserIn(self.test_user2)
        # TODO: Jenny should use the search feature to find the user
        self.browser.get(self.live_server_url + reverse('microblog:user_profile',
                                                        kwargs={'pk': self.test_user.pk}))
        self.assertIn(self.test_user.username, self.browser.page_source)
        self.assertIn(self.test_tweet.content, self.browser.page_source)
        self.browser.find_element_by_link_text(self.test_tweet.content).click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse('microblog:entry_detail', kwargs={'pk': self.test_tweet.pk})
        )
        self.assertIn(self.test_user.username, self.browser.page_source)
        self.assertIn(self.test_tweet.content, self.browser.page_source)

