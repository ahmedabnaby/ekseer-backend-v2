from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateUserAPI.as_view()),

    path('users/', views.UserViewSet.as_view()),

    path('login/', views.LoginAPIView.as_view()),
]
