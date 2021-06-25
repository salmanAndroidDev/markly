from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import Profile
from actions.models import Action


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        """Remove password from being updated"""
        if validated_data.get('password'):
            validated_data.pop('password')
        return super(UserSerializer, self).update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer
    """
    photo = serializers.ImageField(required=False)
    user = UserSerializer(required=True, many=False)
    canonical_url = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'canonical_url')
        read_only_fields = ('id',)

    def get_canonical_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        validated_user_data = validated_data.pop('user')
        user = get_user_model().objects.create_user(
            **validated_user_data)
        return Profile.objects.create(user=user,
                                      **validated_data)

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        self.fields['user'].update(instance=instance.user,
                                   validated_data=user)
        return super(ProfileSerializer, self).update(instance,
                                                     validated_data)
