from django.contrib.auth import get_user_model  # type: ignore
from django.test import TestCase, Client  # type: ignore
from django.urls import reverse  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from .backends import EmailBackend
from .models import ExtendUser
from .forms import EmailAuthenticationForm


class ExtendUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.extend_user = ExtendUser.objects.create(
            user=self.user,
            company='Test Company',
            job_title='Test Job Title',
            first_name='Test First Name',
            last_name='Test Last Name',
            profile_photo='profile_photos/test_profile_photo.jpg',
            country='Test Country',
            city='Test City',
            phone_number='Test Phone Number',
            linkedin_profile='Test LinkedIn Profile',
            git_hub_profile='Test GitHub Profile'
        )

    def test_extend_user_str_method(self):
        self.assertEqual(str(self.extend_user), self.user.username)

    def test_extend_user_job_title(self):
        self.assertEqual(self.extend_user.job_title, 'Test Job Title')


class EmailBackendTestCase(TestCase):
    def setUp(self):
        self.backend = EmailBackend()
        self.password = 'Testpass2023'
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password=self.password,
            username='testuser'
        )

    def test_authenticate_with_valid_credentials(self):
        user = self.backend.authenticate(
            request=None,
            username='test@example.com',
            password=self.password,
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_username(self):
        user = self.backend.authenticate(
            request=None,
            username='invalid@example.com',
            password=self.password,
        )
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        user = self.backend.authenticate(
            request=None,
            username='test@example.com',
            password='wrong_password',
        )
        self.assertIsNone(user)


class EmailAuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Testpass2023',
            username='testuser'
        )

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'Testpass2023'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct email address and password. "
                                      "Note that both fields may be case-sensitive.")

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "This account is inactive.")


class MyLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass2023',
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
        self.login_url = reverse('login')

    def test_login_form(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTrue(isinstance(response.context['form'], EmailAuthenticationForm))

    def test_valid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'Testpass2023'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTrue(isinstance(response.context['form'], EmailAuthenticationForm))
        self.assertContains(response, 'Please enter a correct email address and password.')
