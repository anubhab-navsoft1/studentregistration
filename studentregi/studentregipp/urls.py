from django.urls import path
from studentregipp import views

urlpatterns = [
    path('studentregister/' , views.StudentRegisterCreateListAPIView.as_view() , name='student-register')
]