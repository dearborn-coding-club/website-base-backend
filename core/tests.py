from django.test import TestCase
from core.models import Note


class NoteTest(TestCase):
    def test_note_content_retrieval_is_successful(self):
        """Note returns content when queried"""
        test_note = Note(content="test_content")
        self.assertEqual(test_note.get_content(), 'test_content')
