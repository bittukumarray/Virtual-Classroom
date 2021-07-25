from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Assignment, Submission
from rest_framework.permissions import IsAuthenticated
from authService.models import UserProfile
from django.core.exceptions import ValidationError
from collections import OrderedDict


class Task(APIView):

    permission_classes = (IsAuthenticated,)

    def getAssignmentsforStudent(self, userProfile):
        obj = Assignment.objects.filter(created_for=userProfile)

        res=[]

        for data in obj:
            eachAssignment = OrderedDict(
                    [('id', data.id),
                    ('publish_at', data.publish_at),
                    ("deadline_at", data.deadline_at),
                    ("description", data.description),
                    ("teacher", data.created_by.user.username)
                     ])
            res.append(eachAssignment)
        return Response({"data":res})             


    def getAssignmentsForTeacher(self, userProfile):
        obj = Assignment.objects.filter(created_by=userProfile)

        res=[]

        for data in obj:

            student_list=[]
            for s in data.created_for.all():
                student_list.append(s.user.username)

            eachAssignment = OrderedDict(
                    [('id', data.id),
                    ('publish_at', data.publish_at),
                    ("deadline_at", data.deadline_at),
                    ("description", data.description),
                    ("student_list", student_list)
                     ])
            res.append(eachAssignment)
        return Response({"data":res}) 


    def get(self, request):

        user = request.user

        userProfile=None

        try:
            userProfile= UserProfile.objects.get(user=user)
        except Exception as e:
            return Response({"msg":"you are neither a teacher nor a student"}, status=status.HTTP_401_UNAUTHORIZED)

        if userProfile.role=="student":
            print("yes")
            return self.getAssignmentsforStudent(userProfile)
        else:
            return self.getAssignmentsForTeacher(userProfile)    

    
    def post(self, request):

        user = request.user

        userProfile= UserProfile.objects.get(user=user)
        if userProfile.role=="student":
            return Response({"msg":"You don't have permission to create an assignment"}, status=status.HTTP_401_UNAUTHORIZED)

        publish_at=None
        deadline_at=None
        student_list=[]
        description=None

        try:
            publish_at=request.data["publish_at"]
            deadline_at=request.data["deadline_at"]
            student_list=request.data["student_list"]
            description=request.data["description"]

            if len(description)==0:
                return Response({"msg":"description cant be empty"}, status=status.HTTP_400_BAD_REQUEST)

            if len(student_list)==0:
                return Response({"msg":"student_list cant be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
            if deadline_at<=publish_at:
                return Response({"msg":"publish date cant be on or after deadline"}, status=status.HTTP_400_BAD_REQUEST)
     

        except:
            return Response({"msg":"wrong data format"}, status=status.HTTP_400_BAD_REQUEST)
        
        
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

    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        user = request.user

        userProfile= UserProfile.objects.get(user=user)
        if userProfile.role=="student":
            return Response({"msg":"You don't have permission to update an assignment"}, status=status.HTTP_401_UNAUTHORIZED)

        publish_at=None
        deadline_at=None
        student_list=[]
        description=None

        try:
            publish_at=request.data["publish_at"]
            deadline_at=request.data["deadline_at"]
            student_list=request.data["student_list"]
            description=request.data["description"]

            if len(description)==0:
                return Response({"msg":"description cant be empty"}, status=status.HTTP_400_BAD_REQUEST)

            if len(student_list)==0:
                return Response({"msg":"student_list cant be empty"}, status=status.HTTP_400_BAD_REQUEST)
            if deadline_at<=publish_at:
                return Response({"msg":"publish date cant be on or after deadline"}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"msg":"wrong data format"}, status=status.HTTP_400_BAD_REQUEST)
        
        obj=None
        try:
            obj = Assignment.objects.get(id=pk, created_by=userProfile)
        except Exception as e:
            return Response({"msg":"data does not exist"}, status=status.HTTP_404_NOT_FOUND)

        obj.publish_at=publish_at
        obj.deadline_at=deadline_at
        obj.description=description
        for data in student_list:
            try:
                u=User.objects.get(username=data)
                uProfile = UserProfile.objects.get(user=u)
                obj.created_for.add(uProfile)
            except:
                pass 

        try:       
            obj.save()
        except ValidationError:
            return Response({"msg":"date format is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg":"assignment updated"}, status=status.HTTP_200_OK)    



    def delete(self, request, pk):

        user = request.user

        userProfile= UserProfile.objects.get(user=user)
        if userProfile.role=="student":
            return Response({"msg":"You don't have permission to delete an assignment"}, status=status.HTTP_401_UNAUTHORIZED)
        
        obj=None
        try:
            obj=Assignment.objects.get(id=pk, created_by=userProfile)
            obj.delete()
        except Exception as e:
            return Response({"msg":"data does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"msg":"assignment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






class TaskSubmission(APIView):

    permission_classes = (IsAuthenticated,)

    def getSubmissionForStudent(self, userProfile, assignment_id):

        assignmentObj=Assignment.objects.get(id=assignment_id, created_for=userProfile)

        try:
            assmtDetails={"description":assignmentObj.description, "publish_at":assignmentObj.publish_at, "deadline_at":assignmentObj.deadline_at, "teacher":assignmentObj.created_by.user.username}
            res = Submission.objects.get(user=userProfile, assignment=assignmentObj)
            submissionStatus=None
            if res.submission_date<=assignmentObj.deadline_at:
                submissionStatus="ONTIME SUBMISION"
            else:
                submissionStatus="LATE SUBMISSION"


            return Response({"data":{"assignment_details":assmtDetails,"submission_details":{"submission_id":res.id, "remarks":res.remarks, "submitted_at":res.submission_date,"status":submissionStatus}}})

        except Exception as e:
            return Response({"msg":"no submission for this assignment"}, status=status.HTTP_404_NOT_FOUND)    



    def getSubmissionsForTeacher(self, userProfile, assignment_id):

        assignmentObj=Assignment.objects.get(id=assignment_id, created_by=userProfile)
        res = Submission.objects.filter(assignment=assignmentObj)

        ans=[]

        assmtDetails={"description":assignmentObj.description, "publish_at":assignmentObj.publish_at, "deadline_at":assignmentObj.deadline_at}


        for data in res:
            status=None

            if data.submission_date<=assignmentObj.deadline_at:
                status="ONTIME SUBMISION"
            else:
                status="LATE SUBMISSION"

            eachSubmission = OrderedDict(
                    [('submission_id', data.id),
                    ('remarks', data.remarks),
                    ("student", data.user.user.username),
                    ("submitted_at", data.submission_date),
                    ("status",status),
                     ])
            ans.append(eachSubmission)

        return Response({"data":{"assignment_detaisl":assmtDetails,"submission_details":ans}})         



    def get(self, request, pk):
        
        user = request.user
        userProfile= UserProfile.objects.get(user=user)

        if userProfile.role=="student":
            return self.getSubmissionForStudent(userProfile, pk)
        return self.getSubmissionsForTeacher(userProfile, pk)     

        





    def post(self, request, pk):

        user = request.user

        userProfile= UserProfile.objects.get(user=user)
        if userProfile.role=="teacher":
            return Response({"msg":"You don't have permission to submit an assignment"}, status=status.HTTP_401_UNAUTHORIZED)
        

        remarks = None

        try:
            remarks = request.data["remarks"]
            if len(remarks)==0:
                return Response({"msg":"remarks cant be empty"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"data format incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        assignmentObj = None
        try:
            assignmentObj = Assignment.objects.get(created_for=userProfile, id=pk)
        except:
            return Response({"msg":"assignment does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        obj = None
        
        try:
            obj = Submission.objects.create(user=userProfile, assignment=assignmentObj, remarks=remarks)
        except:
            return Response({"msg":"You have already submitted this assignment so you cant submit again"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"msg":"assignment submitted successfully"}, status=status.HTTP_201_CREATED)