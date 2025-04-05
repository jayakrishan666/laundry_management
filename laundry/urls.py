from django.urls import path
from . import views
from laundry.views import dashboard, request_history

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request-laundry/', views.request_laundry, name='request_laundry'),
    path('admin-requests/', views.admin_laundry_requests, name='admin_requests'),
    path('update-status/<int:request_id>/', views.update_laundry_status, name='update_laundry_status'),
    path('feedback/', views.submit_feedback, name='feedback'),
    path('logout/', views.user_logout, name='logout'),
    path('add-laundry-item/', views.add_laundry_item, name='add_laundry_item'),
    path('delete-laundry-item/<int:item_id>/', views.delete_laundry_item, name='delete_laundry_item'),
    path("history/", request_history, name="history"),
    
    # User Management URLs
    path('user-management/', views.user_management, name='user_management'),
    path('remove-user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('user-history/<int:user_id>/', views.user_history, name='user_history'),

    # Feedback Notification URLs
    path('staff/notifications/', views.admin_notifications, name='admin_notifications'),
    path('staff/feedback/mark-read/<int:feedback_id>/', views.mark_feedback_read, name='mark_feedback_read'),
    path('notifications/', views.notifications, name='notifications'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-notifications-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),

    path('profile/update/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
