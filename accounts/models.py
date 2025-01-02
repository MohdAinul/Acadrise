from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
import secrets
import datetime
# Student model
class Student(models.Model):
    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="N/A")
    pin_code = models.CharField(max_length=6, default="N/A")
    city = models.CharField(max_length=255, default="Unknown")
    student_class = models.CharField(max_length=255, default="N/A")
    address = models.CharField(max_length=255, default="N/A")
    profile_picture = models.ImageField(upload_to='student_pics/', blank=True, null=True)


    def __str__(self):
        return f"Student: {self.user.username}"

# Teacher model
class Teacher(models.Model):
    user = models.OneToOneField(User, related_name='teacher_profile', on_delete=models.CASCADE)

    name = models.CharField(max_length=100, default="N/A")
    pin_code = models.CharField(max_length=6, default="N/A")
    address = models.CharField(max_length=255, default="N/A")
    city = models.CharField(max_length=100, default="N/A")
    profile_picture = models.ImageField(upload_to='teacher_pics/', blank=True, null=True)
    classes_taught = models.CharField(max_length=100, default="N/A")  # e.g., "Grade 8-10"
    subjects = models.CharField(max_length=255, default="N/A")  # e.g., "Math, Science"
    price = models.DecimalField(max_digits=6, decimal_places=2, default=00.00)  # Add Rate field
    about = models.TextField(blank=True, null=True)  # Add About field

    def __str__(self):
        return f"Teacher: {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code_expiry = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    name = models.CharField(max_length=255, blank=True, null=True)
    class_level = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    

    def generate_verification_code(self):
        otp = secrets.randbelow(900000) + 100000  # Secure 6-digit OTP
        self.verification_code = str(otp)
        self.verification_code_expiry = timezone.now() + timezone.timedelta(minutes=5)  # OTP expiry after 5 minutes
        self.save()
        return otp


    def __str__(self):
        return f"{self.user.username}'s Profile"


class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, related_name='sent_connection_requests', on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, related_name='received_connection_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='pending')
                              
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.teacher} | Accepted: {self.is_accepted}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.recipient.username}"



class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True) 
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups", 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",  
        blank=True
    )

