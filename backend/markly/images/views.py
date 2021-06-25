from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from images.serializers import ImageCreateSerializer, ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from images.models import Image
from rest_framework.response import Response
from actions.utils import create_action


class CreateImageView(generics.CreateAPIView):
    """API View to create image"""
    permission_classes = [IsAuthenticated]
    serializer_class = ImageCreateSerializer

    def perform_create(self, serializer):
        new_item = serializer.save(user=self.request.user)
        create_action(self.request.user, 'bookmarked image', new_item)


class MaxinImageView:
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class ImagePagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 2


class RetrieveImageView(MaxinImageView, generics.RetrieveAPIView):
    """API View to retrieve image"""
    pass


class ListImageView(MaxinImageView, generics.ListAPIView):
    """API View to retrieve list of images"""
    pagination_class = ImagePagination


@api_view(['post'])
@login_required
def like_image(request):
    """API View to like | dislike an image"""
    image_id = request.GET.get('id')
    action = request.GET.get('action')

    image = get_object_or_404(Image, id=image_id)

    if action in ('like', 'dislike'):
        if action == 'like':
            image.likes.add(request.user)
            create_action(request.user, 'likes', image)
        else:
            image.likes.remove(request.user)

        return Response(status=status.HTTP_200_OK)
    else:
        error_message = "[Bad action]: action should be ('like', or 'dislike')"
        return Response({'message': error_message}, status.HTTP_406_NOT_ACCEPTABLE)
