from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes, authentication_classes, throttle_classes,
)
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication

from accounts.serializers import ProfileSerializer

User = get_user_model()


class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    # Allow any user (authenticated or not) to access this url
    def post(self, request):
        data = request.data
        serializer = ProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@throttle_classes([UserRateThrottle])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes((ExpiringTokenAuthentication,))
def get_auth_token(request):
    try:
        user = request.user
    except User.DoesNotExist:
        response_data = {"error": "This User account doesn't exist."}
        Response(response_data, status.HTTP_404_NOT_FOUND)

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)
        token.save()

    response_data = {"token": "{}".format(token)}
    return Response(response_data, status=status.HTTP_200_OK)
