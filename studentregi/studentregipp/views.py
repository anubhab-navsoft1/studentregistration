from django.shortcuts import render
from .models import StudentRegister
from .serializers import StudentRegisterSerializer
from rest_framework import generics , status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class StudentRegisterCreateListAPIView(generics.GenericAPIView):
    student_register_serializer_class = StudentRegisterSerializer

    def post(self , request , *args , **kwargs):
        student_register_serializer = self.student_register_serializer_class(data=request.data)
        if student_register_serializer.is_valid():
            email = student_register_serializer.validated_data['email']
            if StudentRegister.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'})
            phone_number = student_register_serializer.validated_data['phone_number']
            if StudentRegister.objects.filter(phone_number=phone_number).exists():
                return Response({'message' : 'Phone number already exists'})
            password = student_register_serializer.validated_data['password']
            student_register_serializer.save()
            hashed_password = make_password(password)
            student_register_serializer.save(password=hashed_password)
            return Response({'message' : 'Student has been created successfully'} , status=status.HTTP_201_CREATED)
        return Response(student_register_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    def get(self , request , *args , **kwargs):
        student = StudentRegister.objects.all()
        student_register_serializer = self.student_register_serializer_class(student , many=True)
        context = {
            "Total Students" : student.count(),
            "Students" : student_register_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)