from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    """A custom user profile to be added to the default django model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers'
    )

    def __str__(self):
        return 'Profile: {}'.format(self.user.username)

# A helper function to automatically create a UserProfile when a user object is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_user_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.get_or_create(user=kwargs.get('instance'))
