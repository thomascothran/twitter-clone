from django.shortcuts import render, HttpResponse

# Create your views here.

def home_page(request):
    context = {}
    return render(request, 'core/homepage.html', context)
