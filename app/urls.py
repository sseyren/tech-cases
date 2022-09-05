from django.urls import path

from .views import CompanyList


urlpatterns = [
    path('company/', CompanyList.as_view()),
]
