from django.test import TestCase
from core.models import Note


class NoteSerializerTest(TestCase):
    def test_note_serializer_works(self):
        """Animals that can speak are correctly identified"""
        test_note = Note(content="test_content")
        self.assertEqual(test_note.get_content(), 'test_content')