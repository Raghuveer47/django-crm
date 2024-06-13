from django.urls import path
from . import views
from .views import create_invoice, view_invoice

urlpatterns = [
    path('', views.home, name='index'),
    path('base/', views.base, name='base'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # CRUD
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-record/', views.create, name='create-record'),
    path('update/<int:pk>', views.update, name='update'),
    path('record/<int:pk>/', views.singular_record, name='record'),  # Ensure this line is correct
    path('upload-csv/', views.upload_csv, name='upload-csv'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),


    #reciept 

     path('receipt/create/', create_invoice, name='create_invoice'),
    path('receipt/<int:pk>/', view_invoice, name='view_invoice'),
]
