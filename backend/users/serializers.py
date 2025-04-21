from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'bio', 'location', 'profile_picture']
        read_only_fields = fields

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None