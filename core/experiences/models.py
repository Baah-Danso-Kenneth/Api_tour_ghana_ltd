from django.db import models
from django.contrib.auth.models import User


class TourGuide(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='guides/', blank=True)

    def __str__(self):
        return self.name



class Experience(models.Model):
    title = models.CharField(max_length=200)
    place_name = models.CharField(max_length=200,null=True,blank=True)
    main_image = models.ImageField(upload_to='experiences/',null=True,blank=True)
    description = models.TextField()
    guide = models.ForeignKey(TourGuide, on_delete=models.SET_NULL, null=True, related_name='experiences')
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    duration_nights = models.PositiveIntegerField(null=True, blank=True)
    base_price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_reverse_season = models.BooleanField(default=False)
    season_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.place_name})"



class TripBatch(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='trip_batches')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField()
    rooms_booked = models.PositiveIntegerField(default=0)

    @property
    def rooms_available(self):
        return self.total_rooms - self.rooms_booked

    @property
    def is_sold_out(self):
        return self.rooms_available <= 0

    def __str__(self):
        return f"{self.experience.title} Trip ({self.start_date} to {self.end_date})"



class Itinerary(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='itineraries/',null=True,blank=True)
    meal_included = models.BooleanField(default=False)
    meal_description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Day {self.day_number} - {self.title}"



class Accommodation(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='accommodations/', null=True, blank=True)

    def __str__(self):
        return self.name


# ✅ Inclusions & Exclusions
class IncludedItem(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='included_items')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Included: {self.text}"


class NotIncludedItem(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='not_included_items')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"Not Included: {self.text}"



class Recommendation(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='recommendations')
    person_name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.person_name}'s Recommendation"



class HistoricalInfo(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='histories')
    content = models.TextField()

    def __str__(self):
        return f"History of {self.experience.place_name}"


class LocationDetails(models.Model):
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, related_name='location_details')
    map_image = models.ImageField(upload_to='locations/')
    best_time_to_visit = models.TextField()
    weather_info = models.TextField()

    def __str__(self):
        return f"Location Details for {self.experience.place_name}"


# 🧾 Booking logic
# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     trip_batch = models.ForeignKey(TripBatch, on_delete=models.CASCADE)
#     number_of_people = models.PositiveIntegerField()
#     payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid')])
#     booked_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Booking for {self.user.username} on {self.trip_batch}"


class MapAndContent(models.Model):
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, related_name='map_details', null=True)
    region_map = models.ImageField(upload_to='maps/', blank=True, null=True)
    best_time_title = models.CharField(max_length=30, blank=True, null=True)
    best_time_des = models.TextField(blank=True, null=True)

    weather_title = models.CharField(max_length=30, blank=True, null=True)
    weather_time_des = models.TextField(blank=True, null=True)