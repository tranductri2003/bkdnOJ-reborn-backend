"""
    Views for auth module
"""

import django_filters
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework import permissions, generics, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view

from helpers.permissions import IsNotAuthenticated
from helpers.custom_pagination import Page50Pagination
from helpers.timezone import datetime_from_z_timestring
from ..serializers import UserDetailSerializer, MyTokenObtainPairSerializer, \
    RegisterSerializer
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """
        TODO: Write docs
    """
    serializer_class = MyTokenObtainPairSerializer


class MyTokenVerifyView(TokenVerifyView):
    """
        Token verify view, receives a JWT token and
        verify if that token is valid. If token is
        valid, returns the corresponding user.
        Basically a debug view that shares the same
        functionality as WhoAmI
    """
    serializer_class = TokenVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            token = request.data['token']
            access_token_obj = AccessToken(token)
            user_id = access_token_obj['user_id']
            user_obj = User.objects.get(id=user_id)

            return Response({
                'user': {
                    'username': user_obj.username,
                    'is_staff': user_obj.is_staff,
                    'is_active': user_obj.is_active,
                }
            }, status=status.HTTP_200_OK)
        except TokenError as err:
            raise InvalidToken(err.args[0]) from err


class WhoAmI(views.APIView):
    """
        If not authenticated, returns {"user": null}
        Look for JWT token at Authentication header and
        return the identity of that user
    """

    def get(self, request, fmat=None):
        """
            GET method
        """
        if request.user.is_authenticated:
            user_obj = request.user
            return Response({
                'user': {
                    'username': user_obj.username,
                    'is_staff': user_obj.is_staff,
                    'is_active': user_obj.is_active,
                }
            }, status=status.HTTP_200_OK)
        return Response({'user': None}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
        Register new account, enforces lowercase alphanum username
    """
    queryset = User.objects.all()
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer


class SignOutView(views.APIView):
    """
        SignOut user, should invalidate their current JWT
        (but not implem yet)
    """

    def get(self, request, fmat=None):
        """
            GET method (TODO: should be POST though!)
        """
        # TODO: Invalidate token
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    """
        List all users in the system. Only staff above can access.
    """

    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = Page50Pagination
    lookup_field = 'username'

    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['^username', '@first_name', '@last_name']
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    ordering_fields = ['date_joined', 'id', 'username']
    ordering = ['-id']

    def get_queryset(self):
        qs = User.objects.all()

        user = self.request.user
        method = self.request.method
        if method == 'GET':
            if user.is_staff and not user.is_superuser:
                qs = qs.filter(is_superuser=False)
        else:
            if not user.is_superuser:
                raise PermissionDenied()

        query_params = self.request.query_params
        date_before = query_params.get('date_joined_before')
        date_after = query_params.get('date_joined_after')

        # TODO: same problem as `submission/views/SubmissionListView.get_queryset()`
        # We are filtering by second-precision, but submission with
        # subtime HH:mm:ss.001 which is greater than HH:mm:ss.000
        # would not be included in the queryset
        # A workaround is to add .999ms the datetimes, basically a way of "rounding"
        # But let's leave it out for now
        try:
            if date_before is not None:
                qs = qs.filter(
                    date_joined__lte=datetime_from_z_timestring(date_before))
            if date_after is not None:
                qs = qs.filter(
                    date_joined__gte=datetime_from_z_timestring(date_after))
        except ValueError:
            pass

        return qs


class ActOnUsersView(views.APIView):
    """
        Act view for User model. Only staff above can call.
        We define Act view as a view that receives `act` payload.
        {
            "method": method_name,
            "data": {
                affected_object_class_1: [...],
                affected_object_class_2: [...],
            }
        }
        The purpose of this view is to optimize command/query that
        is applied on a list of objects.
    """

    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'username'

    ACTION_DEACTIVATE = 'deactivate'
    ACTION_ACTIVATE = 'activate'
    ACTION_DELETE = 'delete'
    AVAILABLE_ACTIONS = [ACTION_DEACTIVATE, ACTION_ACTIVATE, ACTION_DELETE]

    def get_queryset(self):
        """
            get_quertset()
        """
        user = self.request.user
        qs = User.objects.all()
        if not user.has_perm('user.edit_all_users'):
            qs = qs.filter(is_superuser=False)
        return qs

    def post(self, request):
        """
            POST method
        """
        qs = self.get_queryset()
        action = request.data.get('action')
        if action not in ActOnUsersView.AVAILABLE_ACTIONS:
            return Response({
                'message': f"Unrecognized action '{action}'",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.get('data', {})
        usernames = data.get('users', [])
        users = qs.filter(username__in=usernames)

        if action == ActOnUsersView.ACTION_ACTIVATE:
            with transaction.atomic():
                for user in users:
                    user.is_active = True
                User.objects.bulk_update(users, ['is_active'])
        elif action == ActOnUsersView.ACTION_DEACTIVATE:
            with transaction.atomic():
                for user in users:
                    user.is_active = False
                User.objects.bulk_update(users, ['is_active'])
        elif action == ActOnUsersView.ACTION_DELETE:
            users.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Get a certain user, based on `username`.
        Only staff above can call.
        Only admin can make changes to that user.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'username'

    def get_queryset(self):
        qs = User.objects.all()

        user = self.request.user
        method = self.request.method
        if method == 'GET':
            if not user.is_superuser:
                qs = qs.filter(is_superuser=False)
        else:
            if not user.is_superuser:
                raise PermissionDenied()
        return qs


@api_view(['POST'])
def reset_password(request, username):
    """
        Reset password view.
        Only user modifies their password.
        Otherwise only superuser may change.
    """
    user = get_object_or_404(User, username=username)
    if (not request.user.is_superuser) or (not user != request.user):
        raise PermissionDenied()

    password = request.data.get('password', None)
    password2 = request.data.get('password', None)
    if password is None or password2 is None:
        return Response({
            'detail': "'password' and 'password_confirm' cannot be empty."
        }, status=status.HTTP_400_BAD_REQUEST)
    if password != password2:
        return Response({
            'detail': "'password' and 'password_confirm' must not be different."
        }, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    return Response({}, status=status.HTTP_204_NO_CONTENT)


@ensure_csrf_cookie
def get_csrf(request):
    """
        Get CSRF. Unused
    """
    raise NotImplementedError
    # response = JsonResponse({'detail': 'CSRF cookie set'},
    # status=status.HTTP_200_OK)
    # response['X-CSRFToken'] = get_token(request)
    # return response
