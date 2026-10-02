from django.urls import path

from studioclock.views.clock import ClockCreateView, ClockListView

app_name = "clock"

urlpatterns = [
    path("create/", ClockCreateView.as_view(), name="create"),
    path("", ClockListView.as_view(), name="list"),
]
