from rest_framework import serializers
from actions.models import Action


class ActionSerializer(serializers.ModelSerializer):
    """Serializer for Action model"""
    action = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ('action',)

    def get_action(self, obj):
        return f"{obj.user} {obj.verb} {obj.target}"
