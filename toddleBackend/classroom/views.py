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
from django.utils import timezone


class Task(APIView):

    permission_classes = (IsAuthenticated,)

    # statusFilter filter assigments based on status -> ALL, PENDING, OVERDUE, SIBMITTED
    def statusFilter(self, userProfile, assignmentObj, statusParam):
        
        res=[]
        if statusParam=="PENDING":
            for data in assignmentObj:
                try:
                    Submission.objects.get(user=userProfile, assignment=data)
                    continue
                except:
                    if data.deadline_at<=timezone.now():
                        continue    

                eachAssignment = OrderedDict(
                        [('id', data.id),
                        ('publish_at', data.publish_at),
                        ("deadline_at", data.deadline_at),
                        ("description", data.description),
                        ("teacher", data.created_by.user.username)
                        ])
                res.append(eachAssignment)


        elif statusParam=="OVERDUE":
            for data in assignmentObj:
                try:
                    Submission.objects.get(user=userProfile, assignment=data)
                    continue
                except:
                    if data.deadline_at>timezone.now():
                        continue    

                eachAssignment = OrderedDict(
                        [('id', data.id),
                        ('publish_at', data.publish_at),
                        ("deadline_at", data.deadline_at),
                        ("description", data.description),
                        ("teacher", data.created_by.user.username)
                        ])
                res.append(eachAssignment)

                
        elif statusParam=="SUBMITTED":
            for data in assignmentObj:
                try:
                    Submission.objects.get(user=userProfile, assignment=data)
                except:
                    continue    

                eachAssignment = OrderedDict(
                        [('id', data.id),
                        ('publish_at', data.publish_at),
                        ("deadline_at", data.deadline_at),
                        ("description", data.description),
                        ("teacher", data.created_by.user.username)
                        ])
                res.append(eachAssignment)


        else:
            for data in assignmentObj:
                eachAssignment = OrderedDict(
                        [('id', data.id),
                        ('publish_at', data.publish_at),
                        ("deadline_at", data.deadline_at),
                        ("description", data.description),
                        ("teacher", data.created_by.user.username)
                        ])
                res.append(eachAssignment)

        return res


    # getAssignmentsforStudent returns all the assignments assigned to the student with filters
    def getAssignmentsforStudent(self, userProfile, publishAt, statusParam):
        obj = None

        if publishAt=="SCHEDULED":
            obj = Assignment.objects.filter(created_for=userProfile, publish_at__gt=timezone.now())
        elif publishAt=="ONGOING":
            obj = Assignment.objects.filter(created_for=userProfile, publish_at__lte=timezone.now())
        else:
            obj = Assignment.objects.filter(created_for=userProfile)

        res=self.statusFilter(userProfile, obj, statusParam)
        return Response({"data":res})             


    # getAssignmentsForTeacher returns all the assigments which the teacher has created based on filters
    def getAssignmentsForTeacher(self, userProfile, publishAt):

        obj = None

        if publishAt=="SCHEDULED":
            print("yes")
            obj = Assignment.objects.filter(created_by=userProfile, publish_at__gt=timezone.now())
        elif publishAt=="ONGOING":
            obj = Assignment.objects.filter(created_by=userProfile, publish_at__lte=timezone.now())
        else:
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


    # get assignment feed - it will differentiate the request whether it has been
    # made by a student or a teacher and returns the appropriate results.
    def get(self, request):

        user = request.user

        publishAt = request.GET.get("publishedAt")
        statusParam = request.GET.get("status")

        userProfile=None

        try:
            userProfile= UserProfile.objects.get(user=user)
        except Exception as e:
            return Response({"msg":"you are neither a teacher nor a student"}, status=status.HTTP_401_UNAUTHORIZED)

        if userProfile.role=="student":
            print("yes")
            return self.getAssignmentsforStudent(userProfile, publishAt, statusParam)
        else:
            return self.getAssignmentsForTeacher(userProfile, publishAt)    

    # creates an assigment, only teachers can access this, not for student
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

    # complete update of an assignemnt by teahers only, no student can access this
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
            return Response({"msg":"You don't have permission to update this assignment"}, status=status.HTTP_401_UNAUTHORIZED)

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



    # deletes an assigment by teachers only, not accessible by student
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
            return Response({"msg":"You don't have permission to delete this assignment"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"msg":"assignment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






class TaskSubmission(APIView):

    permission_classes = (IsAuthenticated,)

    # getSubmissionForStudent returns submission against an assignment for a student
    def getSubmissionForStudent(self, userProfile, assignment_id):

        assignmentObj = None
        try:
            assignmentObj=Assignment.objects.get(id=assignment_id, created_for=userProfile)
        except:
            return Response({"msg":"this assignment does not exist"}, status=status.HTTP_404_NOT_FOUND)

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



    # getSubmissionsForTeacher returns all the submissions made against an assignment
    def getSubmissionsForTeacher(self, userProfile, assignment_id):

        assignmentObj = None
        try:
            assignmentObj=Assignment.objects.get(id=assignment_id, created_by=userProfile)
        except:
            return Response({"msg":"this assignment does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        res = Submission.objects.filter(assignment=assignmentObj)
        
        ans=[]

        assmtDetails={"description":assignmentObj.description, "publish_at":assignmentObj.publish_at, "deadline_at":assignmentObj.deadline_at}


        for data in res:
            statusRes=None

            if data.submission_date<=assignmentObj.deadline_at:
                statusRes="ONTIME SUBMISION"
            else:
                statusRes="LATE SUBMISSION"

            eachSubmission = OrderedDict(
                    [('submission_id', data.id),
                    ('remarks', data.remarks),
                    ("student", data.user.user.username),
                    ("submitted_at", data.submission_date),
                    ("status",statusRes),
                     ])
            ans.append(eachSubmission)
        if len(ans)==0:
            return Response({"msg":"no submission for this assignment"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data":{"assignment_detaisl":assmtDetails,"submission_details":ans}})         



    # get submissions/submission based on request, it identifies who made the request and sends results appropriately
    def get(self, request, pk):
        
        user = request.user
        userProfile= UserProfile.objects.get(user=user)

        if userProfile.role=="student":
            return self.getSubmissionForStudent(userProfile, pk)
        return self.getSubmissionsForTeacher(userProfile, pk)     

        


    # submits a submission for an assignment, accessible by only student not any teacher
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
            return Response({"msg":"You don't have permission to submit this assignment"}, status=status.HTTP_401_UNAUTHORIZED)
        
        obj = None
        
        try:
            obj = Submission.objects.create(user=userProfile, assignment=assignmentObj, remarks=remarks)
        except:
            return Response({"msg":"You have already submitted this assignment so you cant submit again"},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"msg":"assignment submitted successfully"}, status=status.HTTP_201_CREATED)