from django.urls import path

from .views import (
    CompanyView,
    CompanyListView,
)


urlpatterns = [
    path('company/', CompanyListView.as_view()),
    path('company/<int:pk>/', CompanyView.as_view()),
]
