from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')  # Redirects to the login page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='home'),  # Redirect to login
    path('', include('laundry.urls')),
]