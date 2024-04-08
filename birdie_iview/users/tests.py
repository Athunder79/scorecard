from django.test import TestCase
from users.models import User
from users.forms import UserUpdateForm, UserRegisterForm

# Create your tests here.

class UserFormsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='password')

    def test_user_register_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'django1234',
            'password2': 'django1234'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
    }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
