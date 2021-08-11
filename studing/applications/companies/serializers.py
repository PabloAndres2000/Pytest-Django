from django.db import models
from rest_framework import serializers
from rest_framework.utils import field_mapping
from applications.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "status", "application_link", "last_update", "notes"]
