Django Blog
===========

Django Blog is a Django app that allows you to create and manage blog applications.

Quick Start
-----------

1. Install the package from PyPI:

   .. code-block:: bash

      pip install drf-blog

2. Add "blog" to the `INSTALLED_APPS` setting in your project's `settings.py` file:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          "django_summernote",
          "rest_framework",
          "blog",
      ]

3. Include the blog's URLs by adding the following line to your project's `urls.py` file:

   .. code-block:: python

      from django.urls import path, include

      urlpatterns = [
          ...
          path("", include("blog.urls")),
      ]

4. Set up the necessary media and static file configurations in your project's `settings.py` file:

   .. code-block:: python

      MEDIA_URL = '/media/'
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
      STATIC_ROOT = os.path.join(BASE_DIR, 'static')
      STATIC_URL = "static/"

5. Run database migrations to create the Blog models:

   .. code-block:: bash

      python manage.py migrate

Now you are ready to use the Django Blog app in your project.
