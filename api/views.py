"""API views."""

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class ObtainAuthTokenAndUser(ObtainAuthToken):
    """Return user along with token."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.pk,
                'is_admin': user.is_superuser,
            }
        })


obtain_auth_token = ObtainAuthTokenAndUser.as_view()
