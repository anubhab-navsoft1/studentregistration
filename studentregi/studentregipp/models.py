from django.db import models

class StudentRegister(models.Model):
    gender_choices = (
        ('Male' , 'Male'),
        ('Female' , 'Female'),
        ('Others' , 'Others')
    )
    username = models.CharField(max_length=100 , unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveBigIntegerField()
    gender = models.CharField(max_length=20 , choices=gender_choices)
    email = models.EmailField(max_length=255 , unique=True)
    phone_number = models.CharField(max_length=100 , unique=True)
    password = models.CharField(max_length=255)
    
