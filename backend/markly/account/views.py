from django.contrib.auth.decorators import login_required
from rest_framework import generics
from account.serializers import ProfileSerializer

from account.models import Profile
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserMixinView:
    """
    Mixin class for User Views
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class CreateUserView(UserMixinView, generics.ListCreateAPIView):
    """
    API View to handle User & Profile creating
    """
    pass


class UpdateUserView(UserMixinView, generics.RetrieveUpdateDestroyAPIView):
    """
    API View to handle User & Profile retrieve, update, destroy
    """
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


@login_required
@api_view(['GET'])
def dashboard(request):
    return Response('Hello world')
