from django.contrib import admin
from .models import Attendance, Availability, Event, EventShift

class ShiftInline(admin.TabularInline):
    model = EventShift
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "committee", "starts_at", "status")
    list_filter = ("status", "committee")
    search_fields = ("title", "location")
    inlines = [ShiftInline]

admin.site.register(Availability)
admin.site.register(Attendance)
