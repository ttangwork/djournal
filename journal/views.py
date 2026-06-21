from django.shortcuts import render
from .models import Entry

def entry_list(request):
    entries = Entry.objects.all().order_by('-created_at')
    return render(request, 'journal/entry_list.html', {'entries': entries})

