from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog import views

router = DefaultRouter()
router.register(r"blog", views.BlogViewSet, basename="blog")

urlpatterns = [
    path("summernote/", include("django_summernote.urls")),
    path("api/", include(router.urls)),
]
