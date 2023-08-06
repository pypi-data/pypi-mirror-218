from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog


class BlogAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the Blog model.
    """

    def get_content(self, obj):
        return obj.content[:120]

    get_content.short_description = "content"

    list_display = ["title", "author", "get_content", "attachment"]
    summernote_fields = ("content",)


admin.site.register(Blog, BlogAdmin)
