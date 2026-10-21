from rest_framework import serializers
from .models import Availability, Event, EventShift

class EventShiftSerializer(serializers.ModelSerializer):
    available_count = serializers.SerializerMethodField()
    confirmed_count = serializers.SerializerMethodField()
    class Meta:
        model = EventShift
        fields = ["id", "title", "starts_at", "ends_at", "volunteers_needed", "available_count", "confirmed_count"]
    def get_available_count(self, obj):
        return obj.availability.filter(status=Availability.Status.AVAILABLE).count()
    def get_confirmed_count(self, obj):
        return obj.availability.filter(status=Availability.Status.CONFIRMED).count()

class EventSerializer(serializers.ModelSerializer):
    committee_name = serializers.CharField(source="committee.name", read_only=True)
    shifts = EventShiftSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ["id", "title", "description", "committee", "committee_name", "starts_at", "ends_at", "location", "status", "shifts"]

class AvailabilitySerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source="volunteer.get_full_name", read_only=True)
    shift_title = serializers.CharField(source="shift.title", read_only=True)
    class Meta:
        model = Availability
        fields = ["id", "shift", "shift_title", "volunteer_name", "status", "note", "updated_at"]
        read_only_fields = ["id", "volunteer_name", "shift_title", "updated_at"]
    def validate_status(self, value):
        if value == Availability.Status.CONFIRMED:
            raise serializers.ValidationError("تأكيد الفترة من صلاحية منسق الفعالية فقط.")
        return value
    def create(self, validated_data):
        return Availability.objects.update_or_create(
            shift=validated_data["shift"], volunteer=self.context["request"].user,
            defaults={"status": validated_data.get("status", Availability.Status.AVAILABLE), "note": validated_data.get("note", "")},
        )[0]
