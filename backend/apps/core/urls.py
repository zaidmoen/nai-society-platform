from django.urls import path
from .views import CsrfView, RegisterView, SessionView

urlpatterns = [path("auth/csrf/", CsrfView.as_view()), path("auth/register/", RegisterView.as_view()), path("auth/session/", SessionView.as_view())]
