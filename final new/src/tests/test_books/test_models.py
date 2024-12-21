from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Author, Genre, Book


class BookModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='Test Author',
            biography='Test Biography'
        )
        self.genre = Genre.objects.create(
            name='Test Genre',
            description='Test Description'
        )
        self.book = Book.objects.create(
            title='Test Book',
            description='Test Description',
            owner=self.user,
            pickup_location='Test Location'
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.status, 'available')
        self.assertEqual(self.book.authors.first(), self.author)
        self.assertEqual(self.book.genres.first(), self.genre)
