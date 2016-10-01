from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.

def follow_user(request, pk):
    user_to_follow = get_user_model().objects.get(pk=pk)
    request.user.userprofile.following.add(user_to_follow.userprofile)
    request.user.userprofile.save()
    messages.success(
        request,
        "You are following {}".format(user_to_follow.username)
    )
    return redirect(
        reverse('microblog:user_profile',
        kwargs={'pk': pk})
    )
