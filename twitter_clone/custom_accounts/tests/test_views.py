from django.test import TransactionTestCase, Client
from django.contrib.auth import get_user_model


TEST_USER = {
    'username': 'dafhgeljw',
    'password': 'sarjla3*)(#J',
    'email': 'asdklfjwe@gmail.com',
}


class LoginTest(TransactionTestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            TEST_USER['username'], TEST_USER['email'], TEST_USER['password']
        )

