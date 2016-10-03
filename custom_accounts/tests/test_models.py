from django.test import TransactionTestCase
from django.contrib.auth import get_user_model

from .. import models

TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}


class UserProfileTests(TransactionTestCase):

    def test_whether_user_profile_created_on_user_creation_signal(self):
        django_user_model = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )
        custom_profile = models.UserProfile.objects.get(user=django_user_model)
        self.assertEqual(custom_profile.user, django_user_model)