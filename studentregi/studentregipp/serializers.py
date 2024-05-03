from rest_framework import serializers
from .models import StudentRegister
from django.contrib.auth import authenticate


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegister
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone_number', 'password']
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = StudentRegister.objects.create_user(**validated_data)
    #     return user

class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect username or password.")

            if not user.is_active:
                raise serializers.ValidationError("User is inactive.")

        else:
            raise serializers.ValidationError("Both username and password are required.")

        attrs['user'] = user
        return attrs