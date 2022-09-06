from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from django_filters import rest_framework as filters

from .serializers import CompanySerializer, FollowSerializer
from .models import Company


class CompanyFilter(filters.FilterSet):
    min_employee = filters.NumberFilter(field_name="employee_count", lookup_expr='gte')
    max_employee = filters.NumberFilter(field_name="employee_count", lookup_expr='lte')

    class Meta:
        model = Company
        fields = ['type', 'country']


class CompanyListView(generics.ListCreateAPIView):
    """Lists all companies with included filter arguments."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompanyFilter


class CompanyView(generics.RetrieveUpdateDestroyAPIView):
    """CRUD on single company model."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyFollowView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()
    schema = AutoSchema(operation_id_base='follow')

    def get(self, request, *args, **kwargs):
        """Query current follow status of user on this Company object."""
        company = self.get_object()
        try:
            company.likes.get(id=request.user.id)
        except ObjectDoesNotExist:
            follow = False
        else:
            follow = True

        serializer = self.get_serializer(data={'follow': follow})
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Follow company for current user."""
        company = self.get_object()
        company.likes.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Follow company for current user."""
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Unfollow company for current user."""
        company = self.get_object()
        company.likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowingCompanyListView(generics.ListAPIView):
    """Lists all company objects that current user follows."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompanyFilter
    schema = AutoSchema(operation_id_base='followList')

    def get_queryset(self):
        try:
            return Company.objects.filter(likes=self.request.user)
        except TypeError:
            return Company.objects.none()
