# sticky_notes_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import StickyNote
from .forms import StickyNoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

@login_required
def note_list(request):
    notes = StickyNote.objects.filter(user=request.user)
    return render(request, 'sticky_notes/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = StickyNoteForm()
    return render(request, 'sticky_notes/note_form.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(StickyNote, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = StickyNoteForm(instance=note)
    return render(request, 'sticky_notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(StickyNote, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'sticky_notes/note_confirm_delete.html', {'note': note})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('note_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
