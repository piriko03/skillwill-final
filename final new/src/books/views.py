from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Genre, Book, BookRequest
from .serializers import (
    AuthorSerializer, GenreSerializer,
    BookSerializer, BookRequestSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Author name'),
                'biography': openapi.Schema(type=openapi.TYPE_STRING, description='Author biography'),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Genre name'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Genre description'),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
    """
    Managing books.
    Allows listing, creating, updating and deleting books.
    Supports filtering by status, genre ID and author ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'genres', 'authors']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by status (available/reserved/lent)",
                type=openapi.TYPE_STRING,
                enum=['available', 'reserved', 'lent']
            ),
            openapi.Parameter(
                'genres',
                openapi.IN_QUERY,
                description="Filter by genre ID (example: ?genres=1 for Fantasy)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'authors',
                openapi.IN_QUERY,
                description="Filter by author ID (example: ?authors=1 for specific author)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in title and description fields",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by field (prefix with 'ascending_' or 'descending_')",
                type=openapi.TYPE_STRING,
                enum=[
                    'ascending_created_at', 'descending_created_at',
                    'ascending_title', 'descending_title'
                ]
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        ordering = request.query_params.get('ordering', '')
        if ordering.startswith('ascending_'):
            request.query_params._mutable = True
            request.query_params['ordering'] = ordering.replace('ascending_', '')
        elif ordering.startswith('descending_'):
            request.query_params._mutable = True
            request.query_params['ordering'] = f"-{ordering.replace('descending_', '')}"
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description', 'pickup_location'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Book title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Book description'),
                'pickup_location': openapi.Schema(type=openapi.TYPE_STRING,
                                                  description='Where the book can be picked up'),
                'author_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of author IDs (example: [1,2])'
                ),
                'genre_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='List of genre IDs (example: [1,2])'
                ),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status='available')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class BookRequestViewSet(viewsets.ModelViewSet):
    """
    Managing book requests.
    Users can:
    - Request available books
    - View their own requests
    - View requests for books they own
    Book owners can:
    - Accept or reject requests for their books
    """
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BookRequest.objects.none()

        user = self.request.user
        return BookRequest.objects.filter(
            Q(book__owner=user) | Q(requester=user)
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book', 'message'],
            properties={
                'book': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the book you want to borrow'
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Message to the book owner explaining why you want to borrow the book'
                ),
            }
        ),
        operation_description="Request to borrow an available book",
        responses={
            201: 'Request created successfully',
            400: 'Book is not available or trying to request own book',
            403: 'Authentication required',
            404: 'Book not found'
        }
    )
    def create(self, request, *args, **kwargs):
        try:
            book_id = request.data.get('book')
            book = Book.objects.get(id=book_id)

            if book.owner == request.user:
                return Response(
                    {"error": "Cannot request your own book"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if book.status != 'available':
                return Response(
                    {"error": "Book is not available for requests"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return super().create(request, *args, **kwargs)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        method='post',
        operation_description="Accept a book request (only for book owners)",
        responses={
            200: openapi.Response(
                description="Request accepted",
                examples={
                    "application/json": {
                        "status": "request accepted",
                        "message": "Book status updated to 'lent', other requests rejected"
                    }
                }
            ),
            403: 'Not the book owner',
            404: 'Request not found'
        }
    )
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        book_request = self.get_object()

        if book_request.book.owner != request.user:
            return Response(
                {"error": "Only the book owner can accept requests"},
                status=status.HTTP_403_FORBIDDEN
            )

        if book_request.status != 'pending':
            return Response(
                {"error": "Can only accept pending requests"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_request.status = 'accepted'
        book_request.book.status = 'lent'
        book_request.save()
        book_request.book.save()

        # Reject other pending requests
        book_request.book.requests.exclude(id=book_request.id).update(status='rejected')

        return Response({
            "status": "request accepted",
            "message": "Book status updated to 'lent', other requests rejected"
        })

    @swagger_auto_schema(
        method='post',
        operation_description="Reject a book request (only for book owners)",
        responses={
            200: openapi.Response(
                description="Request rejected",
                examples={
                    "application/json": {
                        "status": "request rejected"
                    }
                }
            ),
            403: 'Not the book owner',
            404: 'Request not found'
        }
    )
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        book_request = self.get_object()

        if book_request.book.owner != request.user:
            return Response(
                {"error": "Only the book owner can reject requests"},
                status=status.HTTP_403_FORBIDDEN
            )

        if book_request.status != 'pending':
            return Response(
                {"error": "Can only reject pending requests"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_request.status = 'rejected'
        book_request.save()
        return Response({"status": "request rejected"})
