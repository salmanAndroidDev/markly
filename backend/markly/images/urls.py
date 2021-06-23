from django.urls import path
from images import views

app_name = 'images'

urlpatterns = [
    path('', views.ListImageView.as_view(), name='list'),
    path('create/', views.CreateImageView.as_view(), name='create'),
    path('retrieve/<int:pk>/', views.RetrieveImageView.as_view(), name='retrieve'),
    path('like/', views.like_image, name='like_dislike'),
]
