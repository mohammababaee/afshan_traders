from rest_framework.views import APIView
from rest_framework.response import Response
from trades.models import Trade
from trades.serializers import TradeSerializer  # Assuming you have a serializer for Trade
from rest_framework import status


class TradesAPIView(APIView):

    def get(self, request):
        all_trades = Trade.objects.all()
        serializer = TradeSerializer(all_trades, many=True)
        return Response({"trades": serializer.data})
    
    def post(self, request):
        trade_data = request.data
        serializer = TradeSerializer(data=trade_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
