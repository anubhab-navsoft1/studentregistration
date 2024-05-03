from rest_framework import serializers
from .models import StudentRegister

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegister
        fields = ['id' , 'username' , 'first_name' , 'last_name' , 'age' , 'gender' , 'email' , 'phone_number' , 'password']
