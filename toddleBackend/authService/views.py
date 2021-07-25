from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import UserProfile


class Signup(APIView):

    
    def createProfile(self, user, role):
        UserProfile.objects.create(user=user, role=role)
        return True


    def post(self, request):

        username = None
        password = None
        role = None
    
        try:
            username = request.data['username']
            password = request.data['password']
            role = request.data['role']
            if not (role=="student"or role=="teacher"):
                return Response({"msg":"role should be either teacher or student"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"data format incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user=User.objects.create(username=username)
            user.set_password(password)
            user.save()
            refresh = RefreshToken.for_user(user)
            if not self.createProfile(user, role):
                return Response({"msg":"something went wrong while creating role"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'refresh': str(refresh),'access': str(refresh.access_token),})
        except:
            return Response({"msg":"This username already exists in the database"}, status=status.HTTP_400_BAD_REQUEST)

