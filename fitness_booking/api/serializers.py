from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Class name cannot be empty.")
        return value

    def validate_instructor(self, value):
        if not value.strip():
            raise serializers.ValidationError("Instructor name cannot be empty.")
        return value

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Date and time must be in the future.")
        return value

    def validate_available_slots(self, value):
        if value < 0:
            raise serializers.ValidationError("Available slots cannot be negative.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_client_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Client name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Client name must be at least 3 characters long.")
        return value

    def validate_client_email(self, value):
        if not value.strip():
            raise serializers.ValidationError("Client email is required.")
        return value

    def validate(self, data):
        fitness_class = data['fitness_class']
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots.")
        
        # Optional: prevent double booking
        if Booking.objects.filter(fitness_class=fitness_class, client_email=data['client_email']).exists():
            raise serializers.ValidationError("You have already booked this class.")

        return data
