from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']
        read_only_fields = ('email',)
