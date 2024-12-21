from django.db import models

from books.models.Author import Author
from books.models.Genre import Genre
from users.models import User


class Book(models.Model):
    class Meta:
        db_table = 'book'

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('lent', 'Lent'),
    ]

    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    pickup_location = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
