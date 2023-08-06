# Django Blog

Django Blog is a Django app that allows you to create and manage blog applications.

# Quick Start
## Usage
After following the Quick Start guide, you're now ready to use the Django Blog app in your project. You can start creating, editing, and managing blog posts through the Django admin panel or through the provided APIs.

1. Install the package from PyPI:

```bash
pip install drf-blog
```

2. Add "blog" to the `INSTALLED_APPS` setting in your project's `settings.py` file:

```python
INSTALLED_APPS = [
    ...
    "django_summernote",
    "rest_framework",
    "blog",
]
```


3. Include the blog's URLs by adding the following line to your project's `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path("", include("blog.urls")),
]
```

4. Set up the necessary media and static file configurations in your project's `settings.py` file:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = "static/"
```

5. Run database migrations to create the Blog models:

```bash
python manage.py migrate
```

Now you are ready to use the Django Blog app in your project.

# Contributing:
Feel free to contribute to this project by submitting issues, fork the project and creating pull requests, or simply by suggesting new features.
# License
This project is licensed under the MIT License
