from django.urls import path
from .views import UserRegistration
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', views.UserRegistration.as_view()),
    path('listing/', views.UserListView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('<int:id>/', views.UserDetailView.as_view())
]

