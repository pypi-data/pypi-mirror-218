from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics
from . import serializers
from .permissions import IsSelfOrReadOnly


class RegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = serializers.EmailUserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]
    serializer_class = serializers.EmailUserSerializer
    queryset = get_user_model().objects.all()
