from rest_framework import serializers
from  core.users.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'created', 'updated', 'email', 'avatar']
        read_only_field = ['is_active']
