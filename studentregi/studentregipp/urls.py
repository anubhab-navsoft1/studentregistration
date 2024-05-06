from django.urls import path
from .views import StudentRegisterCreateListAPIView, StudentLoginAPIView, StudentDetailsRetrieveAPIView

urlpatterns = [
    path('students/', StudentRegisterCreateListAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailsRetrieveAPIView.as_view(), name='student-details'),
    path('login/', StudentLoginAPIView.as_view(), name='login'),
]
