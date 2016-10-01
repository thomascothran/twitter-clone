from django.test import TransactionTestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, resolve

from .. import views


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}
TEST_USER2 = {
    'username': 'dljw',
    'password': 'sa3*)(#J',
    'email': 'we@gmail.com',
}


class FollowUserTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        self.test_user2 = get_user_model().objects.create_user(
            TEST_USER2['username'], TEST_USER2['email'], TEST_USER2['password']
        )

    def test_whether_url_hooked_up_to_view(self):
        client = Client()
        client.force_login(self.test_user)
        found = resolve(reverse('custom_accounts:follow_user', kwargs={'pk': self.test_user2.pk}))
        self.assertEqual(found.func, views.follow_user)


    def test_whether_user_following_view_works(self):
        client = Client()
        client.force_login(self.test_user)
        response = client.get(reverse('custom_accounts:follow_user', kwargs={'pk': self.test_user2.pk}))
        self.assertIn(self.test_user2.userprofile, self.test_user.userprofile.following.all())
        self.assertIn(self.test_user.userprofile, self.test_user2.userprofile.followers.all())
        self.assertRedirects(
            response,
            expected_url=reverse(
                'microblog:user_profile',
                kwargs={'pk': self.test_user2.pk})
        )

    def test_whether_successful_follow_generates_messages(self):
        client = Client()
        client.force_login(self.test_user)
        response = client.get(
            reverse(
                'custom_accounts:follow_user',
                kwargs={'pk': self.test_user2.pk}),
            follow=True
        )
        self.assertIn(
            "You are following {}".format(self.test_user2.username),
            list(response.context['messages'])[0].message
        )
