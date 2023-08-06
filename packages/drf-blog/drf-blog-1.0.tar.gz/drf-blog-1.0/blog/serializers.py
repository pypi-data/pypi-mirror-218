from rest_framework import serializers

from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "short_description",
            "author",
            "state",
            "attachment",
            "read_time",
        ]

    def get_author(self, instance):
        data = {
            "id": instance.author.id,
            "name": f"{instance.author.first_name} {instance.author.last_name}",
        }
        return data
