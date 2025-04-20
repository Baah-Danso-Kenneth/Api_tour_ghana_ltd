from django.db import models


class TourGuide(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    contact = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="guides/", null=True, blank=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='experiences/')
    price_in_sats = models.PositiveIntegerField()
    duration_days = models.IntegerField()
    things_to_bring = models.TextField()
    guide = models.ForeignKey(TourGuide, on_delete=models.SET_NULL, null=True, related_name='experiences')

    def __str__(self):
        return self.title

    def total_cost(self):
        base_price = self.price_in_sats
        room_total = sum([
            room.price_in_sats
            for acc in self.accommodation.all()
            for room in acc.rooms.all()
        ])
        meal_total = self.meal_plan.total_meal_cost() if hasattr(self, 'meal_plan') else 0
        service_fee = self.service_charge.amount_in_sats if hasattr(self, 'service_charge') else 0
        return base_price + room_total + meal_total + service_fee

    def cost_breakdown(self):
        room_total = sum([
            room.price_in_sats
            for acc in self.accommodation.all()
            for room in acc.rooms.all()
        ])
        meal_total = self.meal_plan.total_meal_cost() if hasattr(self, 'meal_plan') else 0

        return {
            "tour": self.price_in_sats,
            "rooms": room_total,
            "meals": meal_total,
            "total": self.price_in_sats + room_total + meal_total
        }


class Itinerary(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.PositiveIntegerField()
    activity_title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.activity_title}"


class Accommodation(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='accommodation')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='accommodations/', null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    quantity_available = models.PositiveIntegerField()
    price_in_sats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.accommodation.name})"


class MealPlan(models.Model):
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, related_name='meal_plan')
    meal_description = models.TextField(help_text="e.g. Breakfast and Lunch provided daily")
    price_per_day_in_sats = models.PositiveIntegerField()
    included_in_package = models.BooleanField(default=True)  # Frontend can use this to hide pricing

    def __str__(self):
        return f"Meal Plan for {self.experience.title}"

    def total_meal_cost(self):
        return self.experience.duration_days * self.price_per_day_in_sats


class ServiceCharge(models.Model):
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, related_name='service_charge')
    amount_in_sats = models.PositiveIntegerField()

    def __str__(self):
        return f"Service charge for {self.experience.title}"
