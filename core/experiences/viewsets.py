from rest_framework import viewsets
from .serializer import (ExperienceSerializer, ExperienceDetailSerializer,
                         NotIncludedItemSerializer, IncludedItemSerializer,
                         TourGuideSerializer, TripBatchSerializer,AccommodationSerializer,
                          RecommendationSerializer, LocationDetailSerializer, ItinerarySerializer,
                          HistoricalInfoSerializer
                         )

from .models import (Experience, NotIncludedItem,
                     TourGuide, HistoricalInfo,
                     Recommendation, Itinerary,Accommodation,
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


class LocationDetailsViewSet(viewsets.ModelViewSet):
    queryset = LocationDetails.objects.all()
    serializer_class = LocationDetailSerializer

class HistoricalInfoViewSet(viewsets.ModelViewSet):
    queryset = HistoricalInfo.objects.all()
    serializer_class = HistoricalInfoSerializer

class NotIncludedItemViewSet(viewsets.ModelViewSet):
    queryset = NotIncludedItem.objects.all()
    serializer_class = NotIncludedItemSerializer

