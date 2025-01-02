
    
# main_app/context_processors.py

from accounts.models import Teacher
from accounts.models import ConnectionRequest

def connection_request_count(request):
    if request.user.is_authenticated:
        try:
            teacher_profile = Teacher.objects.get(user=request.user)
            pending_requests = ConnectionRequest.objects.filter(teacher=request.user, status='pending')
            return {'connection_request_count': pending_requests.count()}
        except Teacher.DoesNotExist:
            return {'connection_request_count': 0}
    return {'connection_request_count': 0}

