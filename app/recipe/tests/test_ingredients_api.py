from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    '''Test the publicly available ingredients API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test: that login is required to access the endpoint'''
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    '''Test the authorized users ingredients API endpoints'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'example@example.com',
            'django123!'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        '''Test: retrieving a list of ingredients'''
        Ingredient.objects.create(user=self.user, name='Beef')
        Ingredient.objects.create(user=self.user, name='Milk')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        '''Test: only ingredients for the authenticated user are returned'''
        other_user = get_user_model().objects.create_user(
            'other-user@example.com',
            'django321!'
        )
        Ingredient.objects.create(user=other_user, name='Vinegar')
        ingredient = Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
