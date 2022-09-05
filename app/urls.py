from django.urls import path

from .views import (
    CompanyView,
    CompanyListView,
    CompanyFollowView,
    FollowingCompanyListView,
)


urlpatterns = [
    path('company/', CompanyListView.as_view()),
    path('company/<int:pk>/', CompanyView.as_view()),
    path('company/<int:pk>/follow/', CompanyFollowView.as_view()),
    path('company/followings/', FollowingCompanyListView.as_view()),
]
