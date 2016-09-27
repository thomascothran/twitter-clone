from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from .models import Entry

# Create your views here.


class BlogEntryCreate(CreateView):
    model = Entry
    fields = ('content', )

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(BlogEntryCreate, self).form_valid(form)

class BlogEntryDetail(DetailView):
    model = Entry

