from apps.clients.models import Clients
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ["passport_id", "passport_date", "country", "city", "blood_group"]
