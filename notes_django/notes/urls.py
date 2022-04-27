from django.urls import path
from .views import NoteListView, NoteDetailView, NoteUpdateView, NoteDeleteView, about, \
    NoteCommonListView, add_note

urlpatterns = [
    path('about/', about, name='about'),
    path('note/new/', add_note, name='note_new'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('', NoteCommonListView.as_view(), name='common'),
    path('home/', NoteListView.as_view(), name='home'),
]