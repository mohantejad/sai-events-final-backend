from rest_framework import serializers
from .models import Event, EventBooking

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.first_name')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'city', 'date', 'created_by', 'event_mode', 'image', 'event_category', 'price', 'created_by', 'number_of_bookings']



class EventBookingSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = EventBooking
        fields = "__all__"
