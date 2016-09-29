from django.test import Client, TransactionTestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth import get_user_model

from .. import views
from .. import models


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}

TEST_USER2 = {
    'username': 'deljw',
    'password': 'sa3*)(#J',
    'email': 'jwe@gmail.com',
}

class BlogCreateEntryTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

    def tearDown(self):
        get_user_model().objects.get(username=TEST_USER['username']).delete()

    def test_url_resolves_to_blog_entry_view(self):
        found = resolve(reverse('microblog:create_entry'))
        self.assertEqual(found.func.view_class, views.BlogEntryCreate)

    def test_view_uses_correct_template(self):
        client = Client()
        response = client.get(reverse('microblog:create_entry'))
        self.assertTemplateUsed(response, 'microblog/entry_form.html')

    def test_that_user_is_related_to_entry_user_created(self):
        test_content = 'SFDKLFJSkwj32qlj'
        client = Client()
        client.force_login(self.test_user)
        data_to_post = {
            'content': test_content
        }
        client.post(
            reverse('microblog:create_entry'),
            data_to_post
        )
        test_entry = models.Entry.objects.get(content=test_content)
        self.assertEqual(
            test_entry.creator,
            self.test_user
        )

    def test_that_user_is_redirected_to_entry_detail_page(self):
        test_content = 'SFDKLFJSkwj32qlj'
        client = Client()
        client.force_login(self.test_user)
        data_to_post = {
            'content': test_content
        }
        response = client.post(
            reverse('microblog:create_entry'),
            data_to_post
        )
        test_entry = models.Entry.objects.get(content=test_content)
        self.assertRedirects(
            response,
            reverse('microblog:entry_detail', kwargs={'pk': test_entry.pk})
        )

class BlogEntryDetailTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_entry = models.Entry.objects.create(
            content='SDLFJWEwlrwjlwlksfd',
            creator=self.test_user,
        )

    def tearDown(self):
        get_user_model().objects.get(username=TEST_USER['username']).delete()

    def test_whether_tweet_attributes_show_up_on_detail_page(self):
        client = Client()
        response = client.get(reverse('microblog:entry_detail', kwargs={'pk': self.test_entry.pk}))
        self.assertContains(response, self.test_entry.content)


class UserProfileViewTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_user2 = get_user_model().objects.create_user(
            TEST_USER2['username'], TEST_USER2['email'], TEST_USER2['password']
        )
        self.test_entry = models.Entry.objects.create(
            content='SDLFJWEwlrwjlwlksfd',
            creator=self.test_user,
        )

    def tearDown(self):
        get_user_model().objects.get(username=TEST_USER['username']).delete()
        get_user_model().objects.get(username=TEST_USER2['username']).delete()

    def test_whether_view_uses_correct_template(self):
        client = Client()
        response = client.get(reverse('microblog:user_profile', kwargs={'pk': self.test_user.pk}))
        self.assertTemplateUsed(response, 'microblog/user_profile.html')

    def test_whether_blog_shows_up_on_creator_users_profile(self):
        client = Client()
        response = client.get(reverse('microblog:user_profile', kwargs={'pk': self.test_user.pk}))
        # Check that tweet content is on page
        self.assertContains(response, self.test_entry.content)
        # Check that link is on page
        self.assertContains(
            response,
            reverse('microblog:entry_detail', kwargs={'pk': self.test_entry.pk})
        )

    def test_whether_username_shows_up_on_creator_users_profile(self):
        client = Client()
        response = client.get(reverse('microblog:user_profile', kwargs={'pk': self.test_user.pk}))
        self.assertContains(response, self.test_user.username)
