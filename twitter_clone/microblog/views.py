from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Entry

# Create your views here.


class BlogEntryCreate(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ('content', )

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(BlogEntryCreate, self).form_valid(form)


class BlogEntryDetail(DetailView):
    model = Entry
    context_object_name = 'entry'


class UserProfile(DetailView):
    model = get_user_model()
    template_name = 'microblog/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['entries'] = Entry.objects.filter(creator=self.object)
        return context


class UserList(ListView):
    model = get_user_model()
    template_name = 'microblog/user_list.html'
