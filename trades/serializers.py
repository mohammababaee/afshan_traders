# trades/serializers.py
from rest_framework import serializers
from trades.models import Trade, Stock, Portfolio


class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Stock
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer): 
    trades = TradeSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = '__all__'
