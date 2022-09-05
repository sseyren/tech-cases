from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
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


class CompanyFollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        try:
            company.likes.get(id=request.user.id)
        except ObjectDoesNotExist:
            follow = False
        else:
            follow = True

        return Response({'follow': follow}, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        company.likes.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        company.likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingCompanyListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompanyFilter

    def get_queryset(self):
        return Company.objects.filter(likes=self.request.user)
