from django.urls import path
from .views import (admin_register, patient_register, UserLoginView, 
                    logout, index, DatasetTableCreateView, DatasetTableListView,user_list, 
                    DatasetTableDetailView, DatasetTableUpdateView, delete_view, predict,ResultListView) 
from django.contrib.auth.views import LogoutView
from django.conf import settings
app_name = "drug_consumption"
urlpatterns = [
    # Admin Perspective
    path('admin-register/',admin_register,name="register-admin"),
    # Patient Perspective
    path('patient-register/',patient_register,name="register-patient"),
    # User
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page="drug_consumption:index"), name="logout"),
    path('',index, name='index'),
    
    # Dataset Perspective
    path('drug-data-create/',DatasetTableCreateView.as_view(),name='drug_data_create'),
    path("drug-data-list/",DatasetTableListView.as_view(),name="drug_data_list"),
    path('drug-data-details/<int:pk>/', DatasetTableDetailView.as_view(),name="drug_data_details"),
    path('drug-data-update/<int:pk>/',DatasetTableUpdateView.as_view(), name="drug_data_update"),
    path("drug-data-delete/<int:pk>/",delete_view, name="drug_data_delete"),
    # Result
    path("predict/<int:pk>/",predict, name='predict'),
    path('results/',ResultListView.as_view(), name='patient_result_list'),
    path("patients/",user_list,name="patient_list"),
]