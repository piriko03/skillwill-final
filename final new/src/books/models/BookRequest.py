from django.db import models
from rest_framework.exceptions import ValidationError


class BookRequest(models.Model):
    class Meta:
        db_table = 'book_request'

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='book_requests')
    message = models.TextField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.book.status != 'available':
            raise ValidationError("This book is not available for requests")
