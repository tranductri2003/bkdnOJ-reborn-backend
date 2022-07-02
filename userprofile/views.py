from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
from django.http import Http404

from .models import UserProfile
from .serializers import UserProfileSerializer, UserProfileBasicSerializer

class UserProfileDetail(generics.RetrieveAPIView):
    """
        Return requested User Profile
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = []
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(self.get_queryset(), user__username=self.kwargs.get('username'))

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs,)

class SelfProfileDetail(generics.RetrieveUpdateAPIView):
    """
        Return user's User Profile, logged-in is required
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def serialize(self, request, data):
        ser_context = { 'request': request, }
        return self.serializer_class(data, context=ser_context)

    def get_object(self, pk):
        if not self.request.user.is_authenticated:
            raise Http404
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object(None)
        return Response(self.serialize(request, profile).data)

    def put(self, request, *args, **kwargs):
        profile = self.get_object(None)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serialize(request, profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        profile = self.get_object(None)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serialize(request, profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = self.get_object(None)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
