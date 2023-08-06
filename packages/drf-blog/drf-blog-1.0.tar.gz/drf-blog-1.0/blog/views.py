from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from blog.models import Blog
from blog.serializers import BlogSerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.filter(state="published")
    permission_classes = (AllowAny,)
    serializer_class = BlogSerializer
