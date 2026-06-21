from django.shortcuts import redirect, render, get_object_or_404
from .models import Entry

def entry_list(request):
    entries = Entry.objects.all().order_by('-created_at')
    return render(request, 'journal/entry_list.html', {'entries': entries})

def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'journal/entry_detail.html', {'entry': entry})

def entry_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        Entry.objects.create(title=title, body=body)
        return redirect('entry_list')
    return render(request, 'journal/entry_form.html')

def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        entry.save()
        return redirect('entry_detail', pk=entry.pk)
    return render(request, 'journal/entry_form.html', {'entry': entry})

def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'journal/entry_confirm_delete.html', {'entry': entry})
