from django.shortcuts import render
from accounts.models import Teacher
from django.contrib.auth.models import User
from accounts.forms import TeacherSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Teacher, ConnectionRequest, ChatMessage,Notification
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponse
from accounts.models import Teacher
from django.shortcuts import render
def home(request):
    teachers = Teacher.objects.order_by('?')[:4]
    
    # Pass teachers and user context
    context = {
        'teachers': teachers,
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'main_app/index.html', context)


def search_teachers(request):
    teachers = None
    if request.method == 'GET':
        form = TeacherSearchForm(request.GET)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            pin_code = form.cleaned_data['pin_code']
            # Filter teachers by subject and pin code
            teachers = Teacher.objects.filter(subjects__icontains=subject, pin_code=pin_code)
    else:
        form = TeacherSearchForm()

    return render(request, 'main_app/search_results.html', {'form': form, 'teachers': teachers})

def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'main_app/teacher_profile.html', {'teacher': teacher})


def index(request):
    return render(request, 'main_app/index.html')

def list_admin_users(request):
    admin_users = User.objects.filter(is_staff=True)
    return render(request, 'main_app/admin_users.html', {'admin_users': admin_users})





@login_required
def send_connection_request(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_user = teacher.user

    # Check if a request already exists
    if not ConnectionRequest.objects.filter(student=request.user, teacher=teacher_user).exists():
        connection_request = ConnectionRequest(student=request.user, teacher=teacher_user)
        connection_request.save()
        messages.success(
            request,
            f"Your connection request has been sent to {teacher.name}. "
            f"Please wait until they accept your request, after which you can chat with {teacher.name}."
        )
        
    
        Notification.objects.create(
            recipient=teacher_user,
            message=f"{request.user.username} has sent you a connection request."
        )
    else:
        messages.info(request, f"You've already sent a request to {teacher.name}.")

    return redirect('teacher_profile', teacher_id=teacher.id)


@login_required
def accept_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id)
    if connection_request.teacher == request.user:
        connection_request.is_accepted = True
        connection_request.save()
    return redirect('connection_requests')




@login_required
def view_connection_requests(request):
    # user is a teacher
    if hasattr(request.user, 'teacher'):
        connection_requests = ConnectionRequest.objects.filter(teacher=request.user, status='pending')
        return render(request, 'main_app/connection_requests.html', {
            'connection_requests': connection_requests
        })
    else:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('index')

@login_required
def accept_connection(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, teacher=request.user)
    if connection_request.status == 'pending':
        connection_request.status = 'accepted'
        connection_request.save()

        Notification.objects.filter(
            recipient=request.user,
            message__icontains=f"{connection_request.student.username} has sent you a connection request."
        ).update(is_read=True)

        messages.success(request, f"You have accepted the connection request from {connection_request.student.username}. You can now chat with them.")
    else:
        messages.info(request, "This connection request has already been handled.")
    return redirect('view_connection_requests')

@login_required
def reject_connection(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, teacher=request.user)
    if connection_request.status == 'pending':
        connection_request.status = 'rejected'
        connection_request.save()

        
        Notification.objects.filter(
            recipient=request.user,
            message__icontains=f"{connection_request.student.username} has sent you a connection request."
        ).update(is_read=True)

        messages.success(request, f"You have rejected the connection request from {connection_request.student.username}.")
    else:
        messages.info(request, "This connection request has already been handled.")
    return redirect('view_connection_requests')

@login_required
def teacher_connection_requests(request):
    if not hasattr(request.user, 'teacher_profile'):
        messages.error(request, "You are not authorized to view connection requests.")
        return redirect('homepage')

    
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')

    
        connection_request = get_object_or_404(
            ConnectionRequest, id=request_id, teacher=request.user, status='pending'
        )

        if action == 'accept':
            connection_request.status = 'accepted'
            connection_request.is_accepted = True
            messages.success(request, "You accepted the connection request.")
        elif action == 'reject':
            connection_request.status = 'rejected'
            messages.success(request, "You rejected the connection request.")
        connection_request.save()

        return redirect('teacher_connection_requests')

    # Fetch all pending connection requests for the logged-in teacher
    pending_requests = ConnectionRequest.objects.filter(teacher=request.user, status='pending')

    return render(request, 'main_app/connection_requests.html', {'pending_requests': pending_requests})

@login_required
def connected_users_list(request):
    # Fetch all accepted connections
    connections = ConnectionRequest.objects.filter(
        (Q(student=request.user) | Q(teacher=request.user)),
        status='accepted'
    )

    # Get unique connected users
    connected_users = set()
    for connection in connections:
        if connection.student == request.user:
            connected_users.add(connection.teacher)
        else:
            connected_users.add(connection.student)
     # Debugging print
    print("Connected Users:", connected_users)
    return render(request, 'main_app/connected_users_list.html', {'connected_users': connected_users})
    


@login_required
def send_message(request, user_id):
    if request.method == "POST":
        other_user = get_object_or_404(User, id=user_id)
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=other_user, message=message_text)
    return redirect('chat_view', user_id=user_id)


@login_required
def chat_view(request, user_id):
    # Get the user to chat with
    other_user = get_object_or_404(User, id=user_id)

    # Fetch chat messages between users
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    return render(request, 'main_app/chat.html', {'other_user': other_user, 'messages': messages})





