# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Blog
from blog.serializers import BlogSerializer

User = get_user_model()


class BlogViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a User
        self.author = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a published blog
        self.published_blog = Blog.objects.create(
            title="Test Blog",
            content="Test content",
            author=self.author,
            short_description="Test description",
            state="published",
        )

        # Create a draft blog
        self.draft_blog = Blog.objects.create(
            title="Draft Blog",
            content="Draft content",
            author=self.author,
            short_description="Draft description",
            state="draft",
        )

    def test_retrieve_published_blog(self):
        url = reverse("blog-detail", args=[self.published_blog.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BlogSerializer(self.published_blog).data)

    def test_retrieve_draft_blog(self):
        url = reverse("blog-detail", args=[self.draft_blog.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_blogs(self):
        url = reverse("blog-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
