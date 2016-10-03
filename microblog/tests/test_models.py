from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from .. import models


# Constants
TEST_ENTRY = {
    'content': 'SDKFJEw42j3klsdslk'
}

class EntryTest(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            'test_user123', 'test_user123@gmail.com', 'afsldkj234234@#!@'
        )
        self.test_entry = models.Entry.objects.create(
            creator=self.test_user,
            content=TEST_ENTRY['content']
        )

    def test_creation_of_entry(self):
        self.assertEqual(
            self.test_entry,
            models.Entry.objects.get(content=TEST_ENTRY['content'])
        )

    def test_that_entry_has_an_absolute_url(self):
        self.assertEqual(
            reverse('microblog:entry_detail', kwargs={'pk': self.test_entry.pk}),
            self.test_entry.get_absolute_url()
        )


