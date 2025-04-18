from rest_framework import routers

from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.users.viewsets import UserViewSet


router = routers.SimpleRouter()

# USERS
router.register(r'user', UserViewSet, basename='user')

#AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename="auth-login")

urlpatterns = [
    *router.urls,
]