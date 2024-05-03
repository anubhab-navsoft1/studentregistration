from django.shortcuts import render
from .models import StudentRegister
from .serializers import StudentRegisterSerializer, StudentLoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class StudentRegisterCreateListAPIView(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if StudentRegister.objects.filter(email=email).exists():
                return Response({'message': 'Email already exists'})
            phone_number = serializer.validated_data['phone_number']
            if StudentRegister.objects.filter(phone_number=phone_number).exists():
                return Response({'message': 'Phone number already exists'})
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response({'message': 'Student has been created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self , request , *args , **kwargs):
        student = StudentRegister.objects.all()
        student_register_serializer = self.student_register_serializer_class(student , many=True)
        context = {
            "Total Students" : student.count(),
            "Students" : student_register_serializer.data
        }
        return Response(context , status=status.HTTP_200_OK)

class StudentLoginAPIView(generics.GenericAPIView):
    serializer_class = StudentLoginSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print("-----------------------", serializer)
    #     if serializer.is_valid():
    #         print("-------------", serializer.is_valid())
    #         user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
    #         print("------------", user)
    #         if user:
    #             refresh = RefreshToken.for_user(user)
    #             return Response({
    #                 'user':serializer.data,
    #                 'refresh': str(refresh),
    #                 'access': str(refresh.access_token),
    #             }, status=status.HTTP_200_OK)
    #         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("-----------------------", serializer)
        if serializer.is_valid():
            print("-------------", serializer.is_valid())
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            print("Attempting to authenticate with username:", password)
            user = authenticate(request, username=username, password=password)
            print("Authentication result:", user)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                print("Authentication failed.")
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
