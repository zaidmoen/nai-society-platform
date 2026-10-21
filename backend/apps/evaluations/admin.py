from django.contrib import admin
from .models import CommitteeNote, Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "committee", "period_label", "status", "created_at")
    list_filter = ("committee", "status", "period_label")
    search_fields = ("volunteer__username", "volunteer__first_name", "volunteer__last_name")

@admin.register(CommitteeNote)
class CommitteeNoteAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "committee", "visibility", "author", "created_at")
    list_filter = ("committee", "visibility")
