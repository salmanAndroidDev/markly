from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from account.serializers import ProfileSerializer
from account.models import Contact
from account.models import Profile
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from actions.utils import create_action
from actions.models import Action

from actions.serializers import ActionSerializer
from django.conf import settings
import redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class UserMixinView:
    """
    Mixin class for User Views
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.filter(user__is_active=True)


class CreateUserView(UserMixinView, generics.ListCreateAPIView):
    """
    API View to handle User & Profile creating
    """

    def perform_create(self, serializer):
        user = serializer.save()
        create_action(user=user, verb='created an account')


class UpdateUserView(UserMixinView, generics.RetrieveUpdateDestroyAPIView):
    """
    API View to handle User & Profile retrieve, update, destroy
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class DetailUserView(UserMixinView, generics.RetrieveAPIView):
    """Detail API View to retrieve User & Profile by id"""
    permission_classes = [AllowAny]
    pass


@login_required
@api_view(['POST'])
def follow(request):
    """View to follower|unfollow a user"""
    id = request.GET.get('profile_id')
    action = request.GET.get('action')
    profile = get_object_or_404(Profile, id=id)

    if id and action in ('follow', 'unfollow'):
        if action == 'follow':
            Contact.objects.get_or_create(follow_from=request.user,  # change it with create
                                          follow_to=profile.user)
            create_action(request.user, 'is following', profile.user)
        else:
            Contact.objects.filter(follow_from=request.user,
                                   follow_to=profile.user).delete()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
    return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class Dashboard(generics.ListAPIView):
    """View to return list of actions"""
    permission_classes = [IsAuthenticated]
    serializer_class = ActionSerializer

    def get_queryset(self):
        followings = self.request.user.following.values_list('username', flat=True)
        r.incr(f'dashboard:view')
        return Action.objects.filter(user__username__in=followings)