from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='example@example.com', password='django123!'):
    '''Create a sample user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test: creating a new user with an email is successful'''
        email = 'example@example.com'
        password = 'django123!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test: the email for a new user is normalized'''
        email = 'example@Example.Com'
        user = get_user_model().objects.create_user(email, 'django123!')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test: creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'django123!')

    def test_create_new_superuser(self):
        '''Test: creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'example@example.com',
            'django123!'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''Test: the tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        '''Test: the ingredient string representation'''
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Egg'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        '''Test: the recipe string representation'''
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Meatballs',
            time_minutes=20,
            price=7.50
        )

        self.assertEqual(str(recipe), recipe.title)
