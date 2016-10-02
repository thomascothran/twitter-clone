from django.shortcuts import render, HttpResponse
from django.db.models import Q


from microblog.models import Entry

# Create your views here.

def home_page(request):
    context = {}
    if request.user.is_authenticated():
        context['posts'] = Entry.objects.filter(
            Q(creator=request.user) |
            Q(creator__userprofile__followers=request.user.userprofile)
        )
    return render(request, 'core/homepage.html', context)
