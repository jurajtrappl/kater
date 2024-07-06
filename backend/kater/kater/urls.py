from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('admin/', admin.site.urls),
]
