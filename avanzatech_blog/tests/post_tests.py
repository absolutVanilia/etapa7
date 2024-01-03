from rest_framework.test import APITestCase, APIClient
from user import models
import pytest
from tests import factories
from django.urls import reverse
from blogs import views
class TestPostCreate(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = factories.UserFactory()
        self.post = factories.PostFactory(owner=self.owner)
        self.endpoint = reverse('create-blog-post')

    def test_endpoint_post_exists(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.endpoint)
        assert response.status_code == 200
    
    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'public', 'writing_permission': 'public'}
        response = self.client.post(self.endpoint, data=data, format='json')
        assert response.status_code == 201

    def test_non_authenticated_user_cannot_create_post(self):
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'public', 'writing_permission': 'public'}
        response = self.client.post(self.endpoint, data=data, format='json')
        assert response.status_code == 403

    def test_create_post_sets_owner_as_logged_user(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'public', 'writing_permission': 'public'}
        response = self.client.post(self.endpoint, data=data, format='json')
        print(response.data)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['content'], 'test')
        self.assertEqual(response.data['reading_permission'], 'public')
        self.assertEqual(response.data['writing_permission'], 'public')
        self.assertTrue(self.owner.posts.filter(id=response.data['id']).exists())

    def test_read_permission_is_restricted_to_public_authenticated_team_and_author(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'wrong', 'writing_permission': 'public'}
        response = self.client.post(self.endpoint, data=data, format='json')
        assert response.status_code == 400

    def test_edit_permission_is_restricted_to_public_authenticated_team_and_author(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'public', 'writing_permission': 'wrong'}
        response = self.client.post(self.endpoint, data=data, format='json')
        assert response.status_code == 400

    def test_read_and_edit_permissions_are_independent_of_each_other(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'test', 'content': 'test', 'reading_permission': 'public', 'writing_permission': 'owner'}
        response = self.client.post(self.endpoint, data=data, format='json')
        self.assertEqual(response.data['reading_permission'], 'public')
        self.assertEqual(response.data['writing_permission'], 'owner')
        assert response.status_code == 201
    
class TestPostEditing(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = factories.UserFactory()
        self.post = factories.PostFactory(owner=self.owner)
        self.endpoint = reverse('update-blog-post', kwargs={'pk': self.post.id})

    def test_dont_allow_changes_to_permissions_content_and_title_by_unauthenticated_user(self):
        post = factories.PostFactory(owner=self.owner, title="test title", content="test content", reading_permission="public", writing_permission="authenticated")
        data = {'title': 'updated title', 'content': 'updated content', 'reading_permission': 'owner', 'writing_permission': 'owner'}
        response = self.client.put(self.endpoint, data=data, format='json')
        assert response.status_code == 403

        post.refresh_from_db()
        self.assertEqual(post.title, 'test title')
        self.assertEqual(post.content, 'test content')
        self.assertEqual(post.reading_permission, 'public')
        self.assertEqual(post.writing_permission, 'authenticated')

    def test_allow_changes_to_permissions_content_and_title_by_author_when_posts_edit_permission_is_authr(self):
        self.client.force_authenticate(user=self.owner)
        post = factories.PostFactory(owner=self.owner, title="test title", content="test content", reading_permission="public", writing_permission="owner")
        endpoint = reverse('update-blog-post', kwargs={'pk': post.id})
        data = {'title': 'updated title', 'content': 'updated content', 'reading_permission': 'owner', 'writing_permission': 'owner'}
        response = self.client.put(endpoint, data=data, format='json')
        assert response.status_code == 200

        post.refresh_from_db()
        self.assertEqual(post.title, 'updated title')
        self.assertEqual(post.content, 'updated content')
        self.assertEqual(post.reading_permission, 'owner')
        self.assertEqual(post.writing_permission, 'owner')





