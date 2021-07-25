from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Assignment
from rest_framework.permissions import IsAuthenticated
from authService.models import UserProfile
from django.core.exceptions import ValidationError


class Task(APIView):

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):

        user = request.user

        publish_at=None
        deadline_at=None
        student_list=[]
        description=None

        try:
            publish_at=request.data["publish_at"]
            deadline_at=request.data["deadline_at"]
            student_list=request.data["student_list"]
            description=request.data["description"]
        except:
            return Response({"msg":"wrong data format"}, status=status.HTTP_400_BAD_REQUEST)
        userProfile= UserProfile.objects.get(user=user)
        if userProfile.role=="student":
            return Response({"msg":"You don't have permission to create an assignment"}, status=status.HTTP_401_UNAUTHORIZED)
        
        obj=None
        try:
            obj = Assignment.objects.create(publish_at=publish_at, deadline_at=deadline_at, description=description, created_by=userProfile)
        except ValidationError:
            return Response({"msg":"date format is not correct"}, status=status.HTTP_400_BAD_REQUEST)
        
        for data in student_list:
            try:
                u=User.objects.get(username=data)
                uProfile = UserProfile.objects.get(user=u)
                obj.created_for.add(uProfile)
            except:
                pass    
        obj.save()
        return Response({"msg":"assignment created"}, status=status.HTTP_201_CREATED)    

class EachTask(APIView):

    def put(self, request, pk):
        pass
