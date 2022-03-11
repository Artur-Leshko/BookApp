from rest_framework import serializers
from books.models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'surname', 'created_at', 'updated_at']

class BookSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'description', 'pages', 'done', 'in_process', 'created_at', 'updated_at']
