from apps.employees.models import Employees
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ["id_employee", "job_title", "specializations", "experience", "education"]
