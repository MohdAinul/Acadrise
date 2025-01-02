from .models import Profile
from django import forms
from .models import Student, Teacher
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UsersignupForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="I am a")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Additional processing can go here if needed
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
  
    class Meta:
        model = Student
        fields = ['name', 'student_class', 'address', 'city', 'pin_code','profile_picture']

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'profile_picture', 'address', 'city', 'classes_taught', 'subjects','price','about','pin_code']




class TeacherSearchForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True, label="Subject")
    pin_code = forms.CharField(max_length=6, required=True, label="Pin Code")
