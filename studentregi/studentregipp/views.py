from django.shortcuts import render
from .models import StudentRegister
from .serializers import StudentRegisterSerializer, StudentLoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class StudentRegisterCreateListAPIView(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer

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
            return Response({'message': 'Student has been created successfully'}, status=status.HTTP_201_CREATED)
        return Response(student_register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self , request , *args , **kwargs):
        student = StudentRegister.objects.all()
        student_register_serializer = self.get_serializer(student , many=True)
        context = {
            "Total Students" : student.count(),
            "Students" : student_register_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)

class StudentLoginAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        student_login_serializer = StudentLoginSerializer(data=request.data)
        if student_login_serializer.is_valid():
            user = student_login_serializer.validated_data['student']
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response(student_login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)