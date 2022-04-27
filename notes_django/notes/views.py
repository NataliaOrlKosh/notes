from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


from .forms import *


def about(request):
    text = """На этом сайте могут оставлять заметки авторизованные пользователи.
    Записи можно делать приватными или публичными."""
    context = {
        'text': text,
    }
    return render(request, 'about.html', context=context)


class NoteListView(ListView):
    model = Note
    template_name = 'home.html'


class NoteCommonListView(ListView):
    model = Note
    template_name = 'common.html'


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    fields = ['title', 'author', 'body', 'photo', 'time_create', 'time_update', 'is_published']


def add_note(request):
    if request.method == 'POST':
        form = AddNoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddNoteForm()
    return render(request, 'note_new.html', {'form': form, 'title': 'Добавление заметки'})


class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'note_edit.html'
    fields = ['title', 'body', 'photo', 'is_published']

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_delete.html'
    success_url = reverse_lazy('home')
