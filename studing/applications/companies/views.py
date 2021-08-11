from applications.companies.models import Company
from rest_framework.viewsets import ModelViewSet
from applications.companies.serializers import CompanySerializer
from rest_framework.pagination import PageNumberPagination


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
