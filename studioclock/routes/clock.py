from django.urls import path

from studioclock.views.clock import ClockListView

app_name = "clock"

urlpatterns = [
    path("", ClockListView.as_view(), name="list"),
]
