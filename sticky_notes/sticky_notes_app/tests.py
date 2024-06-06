from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StickyNote

class StickyNoteModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.stickynote = StickyNote.objects.create(
            title='Test Note',
            content='This is a test note.',
            user=self.user
        )

    def test_stickynote_creation(self):
        self.assertEqual(self.stickynote.title, 'Test Note')
        self.assertEqual(self.stickynote.content, 'This is a test note.')
        self.assertEqual(self.stickynote.user.username, 'testuser')


class StickyNoteViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.stickynote = StickyNote.objects.create(
            title='Test Note',
            content='This is a test note.',
            user=self.user
        )

    def test_stickynote_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertTemplateUsed(response, 'sticky_notes/note_list.html')

    def test_stickynote_create_view(self):
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'This is a new note.'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after creation
        self.assertTrue(StickyNote.objects.filter(title='New Note').exists())

    def test_stickynote_edit_view(self):
        response = self.client.post(reverse('note_edit', args=[self.stickynote.id]), {
            'title': 'Updated Note',
            'content': 'This is an updated note.'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after update
        self.stickynote.refresh_from_db()
        self.assertEqual(self.stickynote.title, 'Updated Note')
        self.assertEqual(self.stickynote.content, 'This is an updated note.')

    def test_stickynote_delete_view(self):
        response = self.client.post(reverse('note_delete', args=[self.stickynote.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect after deletion
        self.assertFalse(StickyNote.objects.filter(id=self.stickynote.id).exists())
