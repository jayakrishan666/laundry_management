from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import LaundryRequest, Feedback
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile

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

        # ✅ Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        # ✅ Check if a UserProfile already exists before creating one
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={"name": name, "phone": phone})

        messages.success(request, "Registration successful! You are now logged in.")
        
        login(request, user)
        return redirect("request_laundry")  

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
from django.shortcuts import get_object_or_404

@staff_member_required
def update_laundry_status(request, request_id):
    """Admin updates laundry request status."""
    laundry_request = get_object_or_404(LaundryRequest, id=request_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        laundry_request.status = new_status
        laundry_request.save()
        return HttpResponseRedirect(reverse('admin_requests'))  # Redirect to admin panel

    return render(request, 'update_status.html', {'laundry_request': laundry_request})

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