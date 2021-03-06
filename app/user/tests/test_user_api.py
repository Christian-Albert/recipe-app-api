from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Test: user API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''Test: creating user with valid payload is successful'''
        payload = {
            'email': 'example@example.com',
            'password': 'django123!',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''Test: creating a user that already exists fails'''
        payload = {
            'email': 'example@example.com',
            'password': 'django123!',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test: that password is more than 5 characters'''
        payload = {
            'email': 'example@example.com',
            'password': '123!',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''Test: that a token is created for the user'''
        payload = {
            'email': 'example@example.com',
            'password': 'django123!'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''Test: that token is not created if invalid credentials are given'''
        payload = {
            'email': 'example@example.com',
            'password': 'django123!'
        }
        create_user(**payload)
        payload_wrong = {
            'email': 'example@example.com',
            'password': 'wrong_password!'
        }
        res = self.client.post(TOKEN_URL, payload_wrong)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''Test: that token is not created if user does not exist'''
        payload = payload = {
            'email': 'example@example.com',
            'password': 'django123!'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''Test: that email and password are required'''
        payload = {
            'email': 'example@example.com',
            'password': 'django123!'
        }
        create_user(**payload)
        payload2 = {
            'email': 'example@example.com'
        }
        res = self.client.post(TOKEN_URL, payload2)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        '''Test: that authentication is required for users'''
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    '''Test API requests that require authentication'''

    def setUp(self):
        self.user = create_user(
            email='example@example.com',
            password='django123!',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        '''Test: retrieving profile for logged in user'''
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_profile_not_allowed(self):
        '''Test: that POST is not allowed on the profile URL'''
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_success(self):
        '''Test: updating the profile for authenticated user successful'''
        payload = {'name': 'New Name', 'password': 'newpassword123!'}
        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
