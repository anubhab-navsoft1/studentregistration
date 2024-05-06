from rest_framework import serializers
from .models import StudentRegister



class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegister
        fields = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone_number', 'password']
      
class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegister
        fields = ['email' , 'password']

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                student = StudentRegister.objects.get(email=email)
            except StudentRegister.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password.', code='authentication')

            attrs['student'] = student
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authentication')

        return attrs