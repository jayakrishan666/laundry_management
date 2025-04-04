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
    path('add-laundry-item/', views.add_laundry_item, name='add_laundry_item'),
    path('delete-laundry-item/<int:item_id>/', views.delete_laundry_item, name='delete_laundry_item'),
    path('request-laundry/', views.request_laundry, name='request_laundry'),
    path("history/", request_history, name="history"),  # New history page
    
    # User Management URLs
    path('user-management/', views.user_management, name='user_management'),
    path('remove-user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('user-history/<int:user_id>/', views.user_history, name='user_history'),
]
