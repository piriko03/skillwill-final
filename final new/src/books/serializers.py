from rest_framework import serializers
from .models import Author, Genre, Book, BookRequest


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    author_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('owner', 'status')

    def create(self, validated_data):
        author_ids = validated_data.pop('author_ids', [])
        genre_ids = validated_data.pop('genre_ids', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(author_ids)
        book.genres.set(genre_ids)
        return book


class BookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'requester', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ('requester', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['book_title'] = instance.book.title
        representation['requester_email'] = instance.requester.email
        return representation
