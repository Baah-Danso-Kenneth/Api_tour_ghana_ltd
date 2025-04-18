from rest_framework import routers

from core.auth.viewsets.register import RegisterViewSet
from core.users.viewsets import UserViewSet

router = routers.SimpleRouter()

# USERS
router.register(r'user', UserViewSet, basename='user')

#AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')

urlpatterns = [
    *router.urls,
]