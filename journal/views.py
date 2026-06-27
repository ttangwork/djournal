from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Entry

@login_required
def entry_list(request):
    query = request.GET.get('q', '')
    entries = Entry.objects.all().order_by('-created_at')
    if query:
        entries = entries.filter(title__icontains=query) | entries.filter(body__icontains=query)
    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'journal/entry_list.html', {'entries': page_obj, 'query': query})

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'journal/entry_detail.html', {'entry': entry})

@login_required
def entry_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        Entry.objects.create(title=title, body=body)
        return redirect('entry_list')
    return render(request, 'journal/entry_form.html')

@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        entry.save()
        return redirect('entry_detail', pk=entry.pk)
    return render(request, 'journal/entry_form.html', {'entry': entry})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'journal/entry_confirm_delete.html', {'entry': entry})
