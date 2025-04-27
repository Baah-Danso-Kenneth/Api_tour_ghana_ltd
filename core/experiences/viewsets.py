from rest_framework import viewsets
from .serializer import (ExperienceSerializer, ExperienceDetailSerializer,
                         NotIncludedItemSerializer, IncludedItemSerializer,
                         TourGuideSerializer, TripBatchSerializer,
                          RecommendationSerializer, LocationDetailSerializer
                         )

from .models import (Experience, NotIncludedItem,
                     TourGuide, HistoricalInfo,
                     Recommendation, Itinerary,
                     IncludedItem, TripBatch, LocationDetails)

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExperienceDetailSerializer
        return ExperienceSerializer


class TourGuideViewSet(viewsets.ModelViewSet):
    queryset = TourGuide.objects.all()
    serializer_class = TourGuideSerializer


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class IncludedItemViewSet(viewsets.ModelViewSet):
    queryset = IncludedItem.objects.all()
    serializer_class = IncludedItemSerializer

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

class TripBatchViewSet(viewsets.ModelViewSet):
    queryset = TripBatch.objects.all()
    serializer_class = TripBatchSerializer


class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = LocationDetails.objects.all()
    serializer_class = LocationDetailSerializer