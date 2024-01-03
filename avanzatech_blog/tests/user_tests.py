from rest_framework.test import APITestCase, APIClient
from user import models
import pytest
from tests import factories
from django.urls import reverse

class TestUserModel:
    @pytest.mark.django_db
    def test_create_user_successfully(self):
        email = 'test@example.com'
        password = 'password123'
        user = models.CustomUser.objects.create_user(email=email, password=password)
    
        assert user.email == email
        assert user.check_password(password)
        assert not user.is_staff
        assert user.is_active
        assert user.team == 1
        assert user.date_joined is not None
        assert user.last_login is not None
        assert str(user) == user.email

    @pytest.mark.django_db
    def test_create_superuser_successfully(self):
        email = 'admin@example.com'
        password = 'admin123'
        superuser = models.CustomUser.objects.create_superuser(email=email, password=password)
    
        assert superuser.email == email
        assert superuser.check_password(password)
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_active
        assert superuser.team == 1
        assert superuser.date_joined is not None
        assert superuser.last_login is not None
    
    @pytest.mark.django_db
    def test_normalize_email(self):
        email = 'Test@Example.com'
        user = models.CustomUser.objects.create_user(email=email)
    
        assert user.email == 'Test@example.com'
    
        # Creating a user without an email should raise a ValueError.
    def test_create_user_without_email_raises_value_error(self):
        with pytest.raises(ValueError):
            models.CustomUser.objects.create_user(email='', password='password123')
    
    @pytest.mark.django_db
    def test_create_superuser_without_is_staff_raises_value_error(self):
        with pytest.raises(ValueError):
            models.CustomUser.objects.create_superuser(email='admin@example.com', password='admin123', is_staff=False)
    
    @pytest.mark.django_db
    def test_create_superuser_without_is_superuser_raises_value_error(self):
        with pytest.raises(ValueError):
            models.CustomUser.objects.create_superuser(email='admin@example.com', password='admin123', is_superuser=False)
    
class Testlogin(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = factories.UserFactory()
        self.post = factories.PostFactory()
        self.endpoint = reverse('login')

    def test_endpoint_login_exists(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        assert response.status_code == 200

class TestLogout(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = factories.UserFactory()
        self.post = factories.PostFactory()
        self.endpoint = reverse('logout')
    
    def test_endpoint_logout_exists(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        assert response.status_code == 302
        assert response.url == 'http://127.0.0.1:8000/user/login'

