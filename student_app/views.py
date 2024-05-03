from django.shortcuts import render
from .models import StudentRegister
from .serializers import StudentRegisterSerializer
from rest_framework import generics , status
from rest_framework.response import Response

# class StudentRegisterCreateListAPIView(generics.GenericAPIView):
