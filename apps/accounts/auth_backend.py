from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class SinglePasswordBackend(BaseBackend):
    """Authenticate using a single shared password for the owner account."""

    def authenticate(self, request, password=None, **kwargs):
        required_password = getattr(settings, "SINGLE_ADMIN_PASSWORD", "1234")
        if not password or password != required_password:
            return None

        User = get_user_model()
        owner = User.objects.filter(role=User.Roles.OWNER).order_by("id").first()
        if owner is None:
            owner = User(
                username="admin",
                role=User.Roles.OWNER,
                is_staff=True,
                is_superuser=True,
                email="",
            )
            owner.set_unusable_password()
            owner.save()
        return owner

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
