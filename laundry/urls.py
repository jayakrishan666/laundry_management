from django.urls import path
from . import views
from laundry.views import dashboard, request_history

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request-laundry/', views.request_laundry, name='request_laundry'),
    path('admin-requests/', views.admin_laundry_requests, name='admin_requests'),
    path('update-status/<int:request_id>/', views.update_laundry_status, name='update_status'),
    path('feedback/', views.submit_feedback, name='feedback'),
    path('logout/', views.user_logout, name='logout'),
    path('aadd-laundry-item/', views.add_laundry_item, name='add_laundry_item'),
    path('request-laundry/', views.request_laundry, name='request_laundry'),
    path("history/", request_history, name="history"),  # New history page
    
]
