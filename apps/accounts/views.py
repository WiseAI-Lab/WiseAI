import jwt
from django.conf import settings
from django.contrib.auth import logout, user_logged_in, get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler

from accounts.serializers import UserRegisterSerializer, UserDetailSerializer

User = get_user_model()


class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    # Allow any user (authenticated or not) to access this url
    def post(self, request):
        user = request.data
        serializer = UserRegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserInfoAPIView(APIView):
    serializer_class = UserDetailSerializer

    def post(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        data = {
            'data': serializer.data,
            'status': 200
        }
        return Response(data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    serializer_class = UserDetailSerializer

    #
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise ValueError
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['username'] = user.username
                user_details['token'] = token
                user_details['message'] = 'success'
                user_details['status'] = 200
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'message': 'can not authenticate with the given credentials or the account has been deactivated',
                'status': 401
            }
            return Response(res, status=status.HTTP_200_OK)
    except KeyError:
        res = {'message': 'please provide a username and a password', 'status': 401}
        return Response(res, status=status.HTTP_200_OK)
    except User.DoesNotExist or ValueError:
        res = {'message': 'username/password error', 'status': 401}
        return Response(res, status=status.HTTP_200_OK)
