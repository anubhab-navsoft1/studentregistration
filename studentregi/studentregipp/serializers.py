from rest_framework import serializers
from .models import StudentRegister
from django.contrib.auth import authenticate


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegister
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone_number', 'password']
      
