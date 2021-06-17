from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
]
