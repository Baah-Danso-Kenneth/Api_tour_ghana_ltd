from rest_framework import routers

from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.refresh import RefreshViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.experiences.viewsets import TourGuideViewSet
from core.payments.viewsets import LightningPaymentViewset, OrderViewSet
from core.shops.viewsets import ProductViewSet
from core.users.viewsets import UserViewSet


router = routers.SimpleRouter()

# USERS
router.register(r'user', UserViewSet, basename='user')

#AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename="auth-login")
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

#Experience
router.register('tour-guides', TourGuideViewSet, basename='tour-guide')
router.register('experiences', ExperienceViewSet, basename='experience')
router.register('trip-batches', TripBatchViewSet, basename='trip-batches')
router.register('itineraries', ItineraryViewSet, basename='itinerary')
router.register('accommodations', AccommodationViewSet, basename='accommodation')
router.register('included-items', IncludedItemViewSet, basename='included-items')
router.register('not-included-items', NotIncludedItemViewSet, basename='not-included-items')
router.register('recommendations', RecommendationViewSet, basename='recommendations')
router.register('histories', HistoricalInfoViewSet, basename='history')
router.register('location-details', LocationDetailsViewSet, basename='location-details')

#Shop
router.register(r'products', ProductViewSet, basename='product')

#Payments
router.register(r'lightning-payments', LightningPaymentViewset, basename='lightning-payment')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    *router.urls,
]