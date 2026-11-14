from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt
from django.test import TestCase
from rest_framework.test import APIClient

from .models import DCCUser, Profile


class AccountAccessTest(TestCase):
    secret = 'test-secret-for-account-access-32-bytes'

    def setUp(self):
        env_patch = patch.dict('os.environ', {'JWT_SECRET': self.secret})
        env_patch.start()
        self.addCleanup(env_patch.stop)
        self.profile = Profile.objects.create(role='user')
        self.other_profile = Profile.objects.create(role='user')
        self.user = DCCUser.objects.create(username='member', profile=self.profile)
        self.client = APIClient()

    def login(self, **extra_claims):
        token = jwt.encode(
            {'id': str(self.user.pk), 'username': self.user.username, **extra_claims},
            self.secret,
            algorithm='HS256',
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_missing_malformed_and_expired_tokens_return_401(self):
        self.assertEqual(self.client.get('/profile/').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer broken')
        self.assertEqual(self.client.get('/me/').status_code, 401)
        self.login(username={})
        self.assertEqual(self.client.get('/me/').status_code, 401)
        self.login(exp=datetime.now(timezone.utc) - timedelta(minutes=1))
        self.assertEqual(self.client.get('/me/').status_code, 401)

    def test_members_can_only_read_and_update_their_own_profile(self):
        self.login()
        self.assertEqual(self.client.get('/me/').json()['username'], 'member')
        self.assertEqual(
            [profile['id'] for profile in self.client.get('/profile/').json()],
            [self.profile.pk],
        )
        self.assertEqual(self.client.get(f'/profile/{self.other_profile.pk}/').status_code, 404)
        self.assertEqual(self.client.get('/user/').status_code, 403)
        response = self.client.patch(
            f'/profile/{self.profile.pk}/', {'about_me': 'Updated', 'role': 'admin'}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['about_me'], 'Updated')
        self.assertEqual(response.json()['role'], 'user')

    def test_members_can_create_notes_but_cannot_delete_shared_notes(self):
        self.login()
        response = self.client.post('/v2/notes/', {'title': 'Notes', 'content': 'Content'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.delete(f"/v2/notes/{response.json()['id']}/").status_code, 403)
