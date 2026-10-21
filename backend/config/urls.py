from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", lambda request: JsonResponse({"status": "ok", "service": "nai-society-api"})),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.committees.urls")),
    path("api/", include("apps.events.urls")),
    path("api/", include("apps.evaluations.urls")),
    path("api/", include("apps.finance.urls")),
]
