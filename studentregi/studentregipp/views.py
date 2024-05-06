from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import StudentRegister
from .serializers import StudentRegisterSerializer, StudentLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StudentRegisterCreateListAPIView(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'phone_number', 'password']
        ),
        responses={
            201: 'Student created successfully',
            400: 'Bad request'
        }
    )
    def post(self, request, *args, **kwargs):
        student_register_serializer = self.get_serializer(data=request.data)
        if student_register_serializer.is_valid():
            email = student_register_serializer.validated_data['email']
            if StudentRegister.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'})
            phone_number = student_register_serializer.validated_data['phone_number']
            if StudentRegister.objects.filter(phone_number=phone_number).exists():
                return Response({'message': 'Phone number already exists'})
            password = make_password(student_register_serializer.validated_data['password'])
            student_register_serializer.validated_data['password'] = password
            student_register_serializer.save()
            return Response({"data" :student_register_serializer.data, 'message': 'Student has been created successfully'}, status=status.HTTP_201_CREATED)
        return Response(student_register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses={
            200: 'List of all registered students'
        }
    )
    def get(self , request , *args , **kwargs):
        student = StudentRegister.objects.all()
        student_register_serializer = self.get_serializer(student , many=True)
        context = {
            "Total Students" : student.count(),
            "Students" : student_register_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)

class StudentLoginAPIView(generics.GenericAPIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: 'Login successful',
            400: 'Bad request'
        }
    )
    def post(self, request, *args, **kwargs):
        student_login_serializer = StudentLoginSerializer(data=request.data)
        if student_login_serializer.is_valid():
            user = student_login_serializer.validated_data['student']
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "data" :student_login_serializer.data })
        else:
            return Response(student_login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailsRetrieveAPIView(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='Student ID')
        ],
        responses={
            200: 'Student details retrieved successfully',
            404: 'Student not found'
        }
    )
    def get(self, request, pk):
        student = get_object_or_404(StudentRegister, pk=pk)
        serializer = self.get_serializer(student)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'phone_number', 'password']
        ),
        responses={
            201: 'Student created successfully',
            400: 'Bad request'
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='Student ID')
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'phone_number', 'password']
        ),
        responses={
            200: 'Student details updated successfully',
            400: 'Bad request',
            404: 'Student not found'
        }
    )
    def put(self, request, pk):
        student = get_object_or_404(StudentRegister, pk=pk)
        serializer = self.get_serializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='Student ID')
        ],
        responses={
            204: 'Student deleted successfully',
            404: 'Student not found'
        }
    )
    def delete(self, request, pk):
        student = get_object_or_404(StudentRegister, pk=pk)
        student.delete()
        return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
