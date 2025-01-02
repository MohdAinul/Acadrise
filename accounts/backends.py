from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Check if the input is an email
            if '@' in username:
                # Filter users by email
                users = User.objects.filter(email=username)
            else:
                # Filter users by username
                users = User.objects.filter(username=username)

            # Iterate through matching users and check the password
            for user in users:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user

        except User.DoesNotExist:
            return None

        return None
