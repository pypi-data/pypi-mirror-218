from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


def upload_location(instance, filename, *args, **kwargs):
    """
    Function to determine the upload location for the Blog attachment.

    Args:
        instance: The instance of the Blog model.
        filename (str): The original filename of the attachment.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        str: The file path for the attachment.

    """
    file_path = f"blog/{instance.author.id}/{instance.title}-{filename}"
    return file_path


class BlogState(models.TextChoices):
    """
    Choices for the state of a Blog.

    Choices:
        draft: The Blog is in draft state.
        published: The Blog is published.

    """

    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class CreatedUpdatedMixin(models.Model):
    """
    Abstract model mixin to store the creation and update timestamps.

    Attributes:
        created_at (DateTimeField): The timestamp when the instance was created.
        updated_at (DateTimeField): The timestamp when the instance was last updated.

    """

    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override the save method to update the 'updated_at' timestamp.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            object: The saved instance.

        """
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class Blog(CreatedUpdatedMixin):
    """
    Model to represent a Blog post.

    Attributes:
        title (CharField): The title of the Blog post.
        content (TextField): The content of the Blog post.
        short_description (TextField): The short description of the Blog post.
        author (ForeignKey): The author of the Blog post.
        state (CharField): The state of the Blog post.
        attachment (FileField): The attachment file for the Blog post.

    """

    title = models.CharField(max_length=60)
    content = models.TextField("Add Blog Content")
    short_description = models.TextField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=BlogState.choices)
    attachment = models.FileField(upload_to=upload_location)

    def __str__(self):
        """
        Return the string representation of the Blog.

        Returns:
            str: The title of the Blog.

        """
        return self.title

    @property
    def read_time(self):
        """
        Calculate and return the estimated reading time of the Blog.

        Returns:
            str: The estimated reading time in minutes.

        """
        words_per_minute = 200
        read_time_minutes = len(self.content.split()) / words_per_minute
        read_time_minutes = round(read_time_minutes)
        return f"{read_time_minutes} min read"
