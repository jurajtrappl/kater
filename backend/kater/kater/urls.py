from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('user/', views.UserView.as_view(), name="user"),
    path('logout/', views.LogoutView.as_view(), name="logout")
]
