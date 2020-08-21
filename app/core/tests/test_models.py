from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test if creating a new user with an email is successful'''
        email = 'example@example.com'
        password = 'django123!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        '''Test if the email for a new user is normalized'''
        email = 'example@Example.Com'
        user = get_user_model().objects.create_user(email, 'django123!')

        self.assertEqual(user.email, email.lower())
