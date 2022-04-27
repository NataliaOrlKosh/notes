from django import template
from notes.models import *
from django.urls import resolve


register = template.Library()


@register.simple_tag(name='getnotes')
def get_notes(filter=None):
    if not filter:
        return Note.objects.all()
    else:
        return Note.objects.filter(is_published=filter)


@register.inclusion_tag('list_notes.html')
def show_notes(request, auth=True):
    current_url = resolve(request.path_info).url_name
    if not auth:
        urls = [{'title': 'Заметки для всех', 'url_name': 'common'},
                {'title': 'О сайте', 'url_name': 'about'}
                ]
    else:
        urls = [{'title': 'Заметки для всех', 'url_name': 'common'},
                {'title': 'Мои заметки', 'url_name': 'home'},
                {'title': 'Добавить новую запись', 'url_name': 'note_new'},
                {'title': 'О сайте', 'url_name': 'about'}
                ]
    return {'urls': urls, 'current_url': current_url}
