from django.urls import path

from studioclock.views.home import HomeView

app_name = "base"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
