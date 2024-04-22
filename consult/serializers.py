# trades/serializers.py
from rest_framework import serializers
from .models import Consult


class ConsultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consult
        fields = ['requested_user', 'related_portfolio', 'consultant']
