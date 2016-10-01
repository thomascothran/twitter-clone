from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required()
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


@login_required()
def unfollow_user(request, pk):
    user_to_unfollow = get_user_model().objects.get(pk=pk)
    request.user.userprofile.following.remove(user_to_unfollow.userprofile)
    request.user.userprofile.save()
    messages.success(
        request,
        "You are no longer following {}".format(user_to_unfollow.username)
    )
    return redirect(
        reverse('microblog:user_profile',
                kwargs={'pk': pk})
    )
