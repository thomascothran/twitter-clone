from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

# Create your views here.

def follow_user(request, pk):
    user_to_follow = get_user_model().objects.get(pk=pk)
    request.user.userprofile.following.add(user_to_follow.userprofile)
    request.user.userprofile.save()
    return redirect(
        reverse('microblog:user_profile',
        kwargs={'pk': pk})
    )
