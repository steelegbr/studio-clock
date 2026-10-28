from django.urls import path

from studioclock.views.api.lamp import LampUpdateView

urlpatterns = [path("lamps/<slug:slug>/state/", LampUpdateView.as_view(), name="lamp")]
