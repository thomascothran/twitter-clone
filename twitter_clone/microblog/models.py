from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.

class Entry(models.Model):
    content = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Entry: {}".format(self.content[:15])

    def get_absolute_url(self):
        return reverse('microblog:entry_detail',  kwargs={'pk': self.pk})

