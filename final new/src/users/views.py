from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Creates a new user account with provided email, name, password and other details.
    """
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password', 'first_name', 'last_name'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email address (will be used for login)',
                    example='user@example.com'
                ),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username',
                    example='john_doe'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Account password',
                    example='secure_password123'
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='First name',
                    example='John'
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Last name',
                    example='Doe'
                ),
                'age': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='User age',
                    example=25
                ),
                'location': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User location for book pickup/delivery',
                    example='New York, NY'
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="User successfully registered",
                examples={
                    "application/json": {
                        "email": "user@example.com",
                        "username": "john_doe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "location": "New York, NY"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "email": ["This email is already registered"],
                        "password": ["This field is required"]
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
