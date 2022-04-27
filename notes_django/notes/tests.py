from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='new_user', email='test@email.com', password='new'
        )

        cls.note = Note.objects.create(
            title='New title',
            body='Content',
            author=cls.user,
        )

    def test_note_model(self):
        self.assertEqual(self.note.title, 'New title')
        self.assertEqual(self.note.body, 'Content')
        self.assertEqual(self.note.author.username, 'new_user')
        self.assertEqual(str(self.note), 'New title')
        self.assertEqual(self.note.get_absolute_url(), '/note/1/')

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/note/1/')
        self.assertEqual(response.status_code, 200)

    def test_note_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content')
        self.assertTemplateUsed(response, 'home.html')

    def test_note_detailview(self):
        response = self.client.get(reverse('note_detail', kwargs={'pk': self.note.pk}))
        no_response = self.client.get('/note/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'New title')
        self.assertTemplateUsed(response, 'note_detail.html')

    def test_post_createview(self):
        response = self.client.post(
            reverse('note_new'),
            {
                'title': 'New title',
                'author': self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.last().title, 'New title')

    def test_note_updateview(self):
        response = self.client.post(
            reverse('note_edit', args='1'),
            {
                'title': 'Updated title',
                'body': 'Updated text',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.last().title, 'Updated title')
        self.assertEqual(Note.objects.last().body, 'Updated text')

    def test_post_deleteview(self):
        response = self.client.post(reverse('note_delete', args='1'))
        self.assertEqual(response.status_code, 302)