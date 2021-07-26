# virtual-classroom

Below I have described each endpoint's response, request, parameters, etc format.



- Sign up  - POST Method

  - It takes username, password and role as input in request body in JSON format and create an user in the db and outputs an access token and a refresh token. Access token can be used to authenticate an user.

    URL -

    ```
     http://localhost:8000/auth/signup/
    ```

    Body format - 

    ```json
    {
        "username":"shubham",
        "password":"123456",
        "role":"student"
    }
    ```

    here role can be either "student" or "teacher"

    Output format - 

    ```json
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNzM3Njg0NCwianRpIjoiNjFkMDdmYTFjMzk2NDVkM2FhZDVjNzIyYTVkMGYxMzciLCJ1c2VyX2lkIjoyNX0.EAxQdC7NYtXITn0T6FZL5Zoe8bxejFGLP8Z3FhT54cI",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3Mzc2ODQ0LCJqdGkiOiI0OGExZGNhMmEyZjQ0ZjgyYWYzMTk0NTRhYjRlOWJhYSIsInVzZXJfaWQiOjI1fQ.mwg0imA8265gwWCjh8d3lG4-c6pWNZMgljcHa277qtE"
    }
    ```

    "access" token can be used to access protected resources.

- Login - POST Method

  - It takes username, password as input in request body in JSON format and outputs an access token and a refresh token. Access token can be used to authenticate an user.

    URL -

    ```
     http://localhost:8000/auth/login/
    ```

    Body format - 

    ```json
    {
        "username":"shubham",
        "password":"123456",
    }
    ```

    here role can be either "student" or "teacher"

    Output format - 

    ```json
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNzM3NzEzMCwianRpIjoiM2U2NzMxODE4ZmIwNDkwYjljNDNhYjA1NDljNWY4NTAiLCJ1c2VyX2lkIjoyNH0.YgaKYRUuE-fCLSsnZRnS9jDIhrJJ1AywtXMxEtzKyaA",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3Mzc3MTMwLCJqdGkiOiI3YWVjYzg5YTZmYzY0NGY0YjJjNWY1YmRkODAzNTFmOCIsInVzZXJfaWQiOjI0fQ.wFI_-_GJVH_4JFwHj3WzMY8jVl7rswqOnX1AGqel4lw"
    }
    ```

    "access" token can be used to access protected resources.

- Create an assignment - POST Method

  - It takes publish_at (datetime), deadline_at (datetime), student_list (list of students username, if any unregistered or wrong username given, it ignore that username and processes for the rest of usernames) and assignment description as input in the request body in JSON format and creates an assignment and assigns to the students_lists.

    URL -

    ```
    http://localhost:8000/classroom/assignment/
    ```

    Body format

    ```json
    {
        "publish_at":"2021-07-26 07:15:10",
        "deadline_at":"2021-07-26 22:15:10",
        "student_list":["shubham", "gollu"],
        "description":"you have to submit this task"
    }
    ```

    Output format

    ```json
    {
        "msg": "assignment created"
    }
    ```

- Update an assignment - PUT Method

  - It takes publish_at (datetime), deadline_at (datetime), student_list (list of students username, if any unregistered or wrong username given, it ignore that username and processes for the rest of usernames) and assignment description as input in the request body in JSON format and assignment id in url as a path parameter and updates the assignment with the given details

    URL - 

    ```
    http://localhost:8000/classroom/assignment/16/
    ```

    Body Format

    ```json
    {
        "publish_at":"2021-07-26 07:15:10",
        "deadline_at":"2021-07-26 07:20:10",
        "student_list":["shubham", "gollu"],
        "description":"updated description"
    }
    ```

    Output Format

    ```json
    {
        "msg": "assignment updated"
    }
    ```

- Get Assignment feed - GET Method

  - when a student makes a request - he/she will get all the assignment assigned to him/her while if teacher makes a request on this endpoint - he/she will get all the assignments he/she has created till now.
  - there are two filters in this method - 
    - both student and teacher can filter assignment based on the publishedAt, we just have to provide key as publishedAt and values as either SCHEDULED or ONGOING in the query param. For the SCHEDULED - it fetched all the assignments which publish_at date time is greater than the current date time, and for the ONGOING - it fetched all the assignments which publish_at date time is less than or equal to the current date time.
    - only for student - status filter. Here status can have any value from ALL, PENDING, OVERDUE, SUBMITTED in the query param. Here ALL means no constraints, PENDING means all the assignments which are not submitted and its deadline is not ended, OVERDUE means all the assignments which are not submitted by the student and the deadline has been passed. SUBMITTED means all the assignments for which the student has a submission.

  URL - 

  ```
  http://localhost:8000/classroom/assignment/
  ```

  Output format for teacher - 

  ```json
  {
      "data": [
          {
              "id": 15,
              "publish_at": "2021-07-26T12:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z",
              "description": "you have to submit this task",
              "student_list": [
                  "gollu",
                  "shubham"
              ]
          },
          {
              "id": 16,
              "publish_at": "2021-07-26T07:15:10Z",
              "deadline_at": "2021-07-26T07:20:10Z",
              "description": "you have to submit this task",
              "student_list": [
                  "gollu",
                  "shubham"
              ]
          },
          {
              "id": 17,
              "publish_at": "2021-07-26T07:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z",
              "description": "you have to submit this task",
              "student_list": [
                  "gollu",
                  "shubham"
              ]
          }
      ]
  }
  ```

  Output format for student -

  ```json
  {
      "data": [
          {
              "id": 15,
              "publish_at": "2021-07-26T12:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z",
              "description": "you have to submit this task",
              "teacher": "bittu ray"
          },
          {
              "id": 16,
              "publish_at": "2021-07-26T07:15:10Z",
              "deadline_at": "2021-07-26T07:20:10Z",
              "description": "you have to submit this task",
              "teacher": "bittu ray"
          },
          {
              "id": 17,
              "publish_at": "2021-07-26T07:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z",
              "description": "you have to submit this task",
              "teacher": "bittu ray"
          }
      ]
  }
  ```

- Delete an assignment - DELETE Method

  - it takes assignment id in the path parameter and deletes the assignment

  URL - 

  ```
  http://localhost:8000/classroom/assignment/16/
  ```

  Here 16 is the assignment id which we want to delete

- Get submission/submissions for an assignment 

  - It behaves different in case of request made by teacher than the request made by student
  - when a teacher makes a request on this endpoint - it returns all the submissions for the given assignment id
  - when a student makes a request on this endpoint - it returns his/her submission for the given assignment

  URL - 

  ```
  http://localhost:8000/classroom/assignment/15/submission/
  ```

  here 15 is the assignment id

  Output when a teacher makes a request on this endpoint

  ```json
  {
      "data": {
          "assignment_detaisl": {
              "description": "you have to submit this task",
              "publish_at": "2021-07-26T12:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z"
          },
          "submission_details": [
              {
                  "submission_id": 3,
                  "remarks": "i have submitted",
                  "student": "gollu",
                  "submitted_at": "2021-07-26T07:56:45.183773Z",
                  "status": "ONTIME SUBMISION"
              }
          ]
      }
  }
  ```

  Output when a student makes a request on this endpoint

  ```json
  {
      "data": {
          "assignment_details": {
              "description": "you have to submit this task",
              "publish_at": "2021-07-26T12:15:10Z",
              "deadline_at": "2021-07-26T22:15:10Z",
              "teacher": "bittu ray"
          },
          "submission_details": {
              "submission_id": 3,
              "remarks": "i have submitted",
              "submitted_at": "2021-07-26T07:56:45.183773Z",
              "status": "ONTIME SUBMISION"
          }
      }
  }
  ```

- Add a submission for an assignment  -  POST Method

  - it takes remarks as input in JSON format and creates a submission for the student for the assignment

  URL -

  ```
  http://localhost:8000/classroom/assignment/15/submission/
  ```

  Body Format 

  ```json
  {
      "remarks":"i have submitted"
  }
  ```

  here remarks can't be empty since it is the answer of the assignment



All the cases like a student can't create/update any assignment, a teacher can not submit any assignment, any teacher can't access any other teacher's assignment, any student can't access any other student's assignment and submission, etc have been handled.