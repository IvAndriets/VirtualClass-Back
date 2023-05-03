from rest_framework import generics, permissions
from user.serializers import UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    keycloak_scopes = {
        'DEFAULT': 'User:manage'
    }

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
