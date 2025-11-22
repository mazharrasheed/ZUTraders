from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User

class BypassAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if getattr(settings, "BYPASS_AUTH", False):
            # Create or use a fake superuser
            try:
                fake_user = User.objects.filter(is_superuser=True).first()
            except:
                fake_user = None

            request.user = fake_user or AnonymousUser()
            request._cached_user = request.user

        return self.get_response(request)
