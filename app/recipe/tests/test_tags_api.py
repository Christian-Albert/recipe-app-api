from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    '''Test the publicly available tags api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test: that login is required for retrieving tags'''
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    '''Test the authorized users tags api'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'example@example.com',
            'django123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        '''Test: retrieving tags'''
        Tag.objects.create(user=self.user, name='Indian')
        Tag.objects.create(user=self.user, name='Vegan')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        '''Test: tags returned are for the authenticated user'''
        other_user = get_user_model().objects.create_user(
            'other-user@example.com',
            'django321!'
        )
        Tag.objects.create(user=other_user, name='Drinks')
        tag = Tag.objects.create(user=self.user, name='Meat')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
