from rest_framework import generics
from django_filters import rest_framework as filters

from .serializers import CompanySerializer
from .models import Company


class CompanyFilter(filters.FilterSet):
    min_employee = filters.NumberFilter(field_name="employee_count", lookup_expr='gte')
    max_employee = filters.NumberFilter(field_name="employee_count", lookup_expr='lte')

    class Meta:
        model = Company
        fields = ['type', 'country']


class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompanyFilter


class CompanyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

