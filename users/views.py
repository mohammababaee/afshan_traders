from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer
from .models import User


class UserAuth(APIView):
    def post(self, request):
        user_data = request.data
        email = user_data.get("email")
        password = user_data.get("password")

        # Create a new user instance
        new_user = User(email=email)

        # Set the password using set_password method
        new_user.set_password(password)

        # Save the user object
        new_user.save()

        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )

    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response({"trades": serializer.data})
