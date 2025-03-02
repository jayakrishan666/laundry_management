from django.db import models
from django.contrib.auth.models import User

class LaundryItem(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

from datetime import datetime

class LaundryRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Recieved', 'Recieved'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(LaundryItem, through='LaundryRequestItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # New Field

    def save(self, *args, **kwargs):
        """Automatically set completed_at when status is changed to 'Completed'."""
        if self.status == "Completed" and self.completed_at is None:
            self.completed_at = datetime.now()
        elif self.status != "Completed":
            self.completed_at = None  # Reset if status changes back
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.username} - {self.status}"
    





class LaundryRequestItem(models.Model):
    laundry_request = models.ForeignKey(LaundryRequest, on_delete=models.CASCADE)
    item = models.ForeignKey(LaundryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.laundry_request.user.username} - {self.item.name} ({self.quantity})"





class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)






from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Phone number field
    
    @property
    def unique_id(self):
        """Return the built-in User ID as the unique identifier."""
        return self.user.id
