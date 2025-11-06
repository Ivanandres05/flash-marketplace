from django.test import TestCase
from django.urls import reverse
from .models import User

class UserAccountTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_login_view(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_registration_view(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())