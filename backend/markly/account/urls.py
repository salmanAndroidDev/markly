from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('detail/<int:pk>/', views.DetailUserView.as_view(), name='detail'),
    path('follow/', views.follow, name='follow'),
]
