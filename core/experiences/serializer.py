from .models import (Experience, Accommodation,
                     TripBatch, TourGuide, Itinerary,
                     IncludedItem, NotIncludedItem, HistoricalInfo,
                     Recommendation, LocationDetails)
from rest_framework import serializers

# Define TourGuideSerializer first
class TourGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourGuide
        fields = ['name', 'bio', 'image']

# Now you can safely reference TourGuideSerializer in other serializers
class ExperienceSerializer(serializers.ModelSerializer):
    guide = TourGuideSerializer(read_only=True)
    class Meta:
        model = Experience
        fields = '__all__'

class IncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncludedItem
        fields = '__all__'

class NotIncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotIncludedItem
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer(read_only=True)
    class Meta:
        model = Recommendation
        fields = '__all__'

class TripBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripBatch
        fields = '__all__'

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'

class ItinerarySerializer(serializers.ModelSerializer):
    experience = ExperienceSerializer(read_only=True)
    class Meta:
        model = Itinerary
        fields = '__all__'

class HistoricalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalInfo
        fields = '__all__'

class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetails
        fields = '__all__'

class ExperienceDetailSerializer(serializers.ModelSerializer):
    itineraries = ItinerarySerializer(many=True, read_only=True)
    accommodations = AccommodationSerializer(many=True, read_only=True)
    included_items = IncludedItemSerializer(many=True, read_only=True)
    not_included_items = NotIncludedItemSerializer(many=True, read_only=True)
    trip_batches = TripBatchSerializer(many=True, read_only=True)
    location_details = LocationDetailSerializer(many=True, read_only=True)
    guide = TourGuideSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = '__all__'
