from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from api.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.get(username=username)
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed()

        payload = {
            "id": user.id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}

        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.get(pk=payload["id"])
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

        return Response(token)