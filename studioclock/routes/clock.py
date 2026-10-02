from django.urls import path

from studioclock.views.clock import ClockCreateView, ClockListView, ClockUpdateView

app_name = "clock"

urlpatterns = [
    path("create/", ClockCreateView.as_view(), name="create"),
    path("<uuid:pk>/edit/", ClockUpdateView.as_view(), name="edit"),
    path("", ClockListView.as_view(), name="list"),
]
