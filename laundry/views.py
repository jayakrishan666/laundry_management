from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import LaundryRequest, Feedback
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import LaundryItem, LaundryRequestItem
import json

# User Registration & Login
def register_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        try:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()

            # Create or get UserProfile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'phone': phone}
            )

            messages.success(request, "Registration successful! You are now logged in.")
            login(request, user)
            return redirect("request_laundry")
            
        except Exception as e:
            # If anything goes wrong, delete the user and show error
            if 'user' in locals():
                user.delete()
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect("register")

    return render(request, "register.html")


def user_login(request):
    """Handles both user and admin login."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Check if the user is an admin
                return redirect('admin_requests')  # Redirect to admin dashboard
            else:
                return redirect('request_laundry')  # Redirect to user dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

# Dashboard
@login_required
def dashboard(request):
    """Show only active laundry requests (hide completed ones)."""
    laundry_requests = LaundryRequest.objects.filter(user=request.user).exclude(status="Completed")
    return render(request, 'dashboard.html', {'requests': laundry_requests})

@login_required
def request_history(request):
    """Show all past laundry requests, including completed ones with their completion date."""
    history_requests = LaundryRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "history.html", {"requests": history_requests})

# Request 
from django.db.models import Q
from .models import LaundryRequest, LaundryItem, LaundryRequestItem

def request_laundry(request):
    """User requests laundry with multiple items."""
    last_request = LaundryRequest.objects.filter(user=request.user).order_by("-created_at").first()

    if last_request and last_request.status != "Completed":
        return render(request, "request_blocked.html")  # Restrict request

    if request.method == "POST":
        selected_items = request.POST.getlist("items")
        quantities = request.POST.getlist("quantities")

        if selected_items and quantities:
            new_request = LaundryRequest.objects.create(user=request.user)

            for i, item_id in enumerate(selected_items):
                item = LaundryItem.objects.get(id=item_id)
                LaundryRequestItem.objects.create(
                    laundry_request=new_request,
                    item=item,
                    quantity=int(quantities[i])
                )

            return redirect("dashboard")

    items = LaundryItem.objects.all()
    return render(request, "request_laundry.html", {"items": items})


# Admin View Requests & Update Status
@staff_member_required
def admin_laundry_requests(request):
    """Admin view to see all laundry requests."""
    requests = LaundryRequest.objects.all().order_by('-created_at')
    return render(request, 'admin_request.html', {'requests': requests})

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import LaundryRequest

@staff_member_required
def update_laundry_status(request, request_id):
    laundry_request = get_object_or_404(LaundryRequest, id=request_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        laundry_request.status = new_status
        laundry_request.save()

        # Send email if status is 'Completed'
        if new_status == 'Completed':
            send_mail(
                'Your Laundry Request is Completed',
                f'Hello {laundry_request.user.username},\n\nYour laundry request (ID: {laundry_request.id}) has been completed successfully, Pick your laundry',
                'your_email@example.com',  # Sender email
                [laundry_request.user.email],  # Receiver email
                fail_silently=False,
            )
            messages.success(request, 'Status updated and email sent successfully!')

        else:
            messages.success(request, 'Status updated successfully!')

        return redirect('admin_requests')

    return render(request, 'update_status.html', {'request': laundry_request})

# Submit Feedback
@login_required
def submit_feedback(request):
    if request.method == "POST":
        rating = request.POST['rating']
        comment = request.POST['comment']
        Feedback.objects.create(user=request.user, rating=rating, comment=comment)
        return redirect('dashboard')
    return render(request, 'feedback.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout



from .models import LaundryItem
@staff_member_required
def add_laundry_item(request):
    """Admin can add new laundry items."""
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            LaundryItem.objects.create(name=name)
            messages.success(request, "Item added successfully!")
            return redirect("add_laundry_item")

    items = LaundryItem.objects.all()
    return render(request, "add_laundry_item.html", {"items": items})

@staff_member_required
def delete_laundry_item(request, item_id):
    """Admin can delete laundry items."""
    try:
        item = LaundryItem.objects.get(id=item_id)
        item.delete()
        messages.success(request, "Item deleted successfully!")
    except LaundryItem.DoesNotExist:
        messages.error(request, "Item not found!")
    return redirect("add_laundry_item")

@staff_member_required
def user_management(request):
    """Admin view for managing users."""
    users = UserProfile.objects.all().select_related('user')
    return render(request, 'user_management.html', {'users': users})

@staff_member_required
@require_POST
def remove_user(request, user_id):
    """Remove a user from the system."""
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@staff_member_required
def user_history(request, user_id):
    """Get the laundry request history for a specific user."""
    try:
        user = User.objects.get(id=user_id)
        requests = LaundryRequest.objects.filter(user=user).order_by('-created_at')
        
        history = []
        for req in requests:
            items = []
            for request_item in req.laundryrequestitem_set.all():
                items.append({
                    'name': request_item.item.name,
                    'quantity': request_item.quantity
                })
            
            history.append({
                'date': req.created_at.strftime('%B %d, %Y'),
                'status': req.status,
                'items': items
            })
        
        return JsonResponse({'success': True, 'history': history})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})