from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .token import *
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import fastapi_client, FastAPIError
# Create your views here.

def homee(r):
    return render(r,'home.html',{'name':'kushi','age':29})

def h1(r):
    return render(r,'h.html',{'name':'ku','age':29})

def about(r):
    return render(r,'about.html',{'name':'kushi','age':29})

def add(r):
    num1 = r.POSTs['num1']
    num2 = r.POSTs['num2']
    res = int(num1) + int(num2)
    return render(r,'result.html',{'result':res})

def student_content(r):
    # s = Student()
    # s.name = 'kushi'
    # s.age = 29
    # s.place = 'New York'

    # s1 = Student()
    # s1.name = 'Emma'
    # s1.age = 22
    # s1.place = 'London'

    # s2 = Student()
    # s2.name = 'John'
    # s2.age = 30
    # s2.place = 'Paris'

    # sf = [s,s1,s2]

    data = StudentDetails.objects.filter(valid = True)
    # print('abc')
    # print(data)

    return render(r,'student.html',{'students' : data})

def Teachers(r):
    # student,create = Teacher.objects.get_or_create(name = 'kjwcbn',feed_back = 'kjhdcuhc')
    # print(student)
    # print(create)

    if r.method == 'POST':
        Teacher.objects.create(
            name = r.POST.get("name"),
            feed_back = r.POST.get("feed_back")
        )
    return render(r,'sucess.html')

def Teacher_update(r,id):
    
    t = Teacher.objects.get(id = id)
    t.name = r.POST['name']
    t.feed_back = r.POST['feed_back']
    t.save()
    return render(r,'sucess.html')

@api_view(['GET'])
def drf(r):
    return Response({'status':200,'message':'thisis def api'})


@api_view(['GET'])
def get_studentdetails(r):
    data = StudentDetails.objects.all()

    serializer = StudentDetailsSerializer(data, many=True)

    return Response({
        'status': 200,
        'data': serializer.data
    })

# @api_view(['POST'])
# def post_data(r):
#     if r.method == 'POST':
#         name = r.data.get('name')
#         age = r.data.get('age')
#         place = r.data.get('place')

#         Student.objects.create(
#             name=name,
#             age=age,
#             place=place
#         )
#     return Response({
#         'status': 200,})

@api_view(['POST'])
def post_data(request):

    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response({
            'status': 200,
            'message': 'Student created successfully'
        })

    return Response({
        'status': 400,
        'errors': serializer.errors
    })

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name
    })

@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:

        refresh = MyToken.for_user(user)
        print(type(refresh))

        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    return Response({
        'message': 'Invalid username or password'
    }, status=401)

class StudentListView(ListAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListView1(UpdateAPIView,DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fastapi_students(request):

    # Grab the same token to forward to FastAPI
    forward_headers = {
        'Authorization': request.headers.get('Authorization')
    }

    try:
        data = fastapi_client.get("/studentss/", headers=forward_headers)      
    except FastAPIError as e:                         
        return Response({"error": str(e)}, status=e.status_code or 502)   
    return Response(data)                             

