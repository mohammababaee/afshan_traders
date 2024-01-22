from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trades.models import Portfolio, Stock, Trade
from trades.serializers import PortfolioSerializer, TradeSerializer
from trades.serializers import StockSerializer


class TradesAPIView(APIView):

    def get(self, request):
        all_trades = Trade.objects.all()
        serializer = TradeSerializer(all_trades, many=True)
        return Response({"trades": serializer.data})

    def post(self, request):
        trade_data = request.data
        portfolio_id = trade_data.get('portfolio')  
        stock_symbol = trade_data.get('stock')  

        trade_serializer = TradeSerializer(data=trade_data)
        if trade_serializer.is_valid():
            
            try:
                stock = Stock.objects.get(symbol=stock_symbol)
            except Stock.DoesNotExist:
                return Response({'error': 'Stock not found'}, status=status.HTTP_400_BAD_REQUEST)

            trade = trade_serializer.save(stock=stock)  
            
            if portfolio_id:
                try:
                    portfolio = Portfolio.objects.get(id=portfolio_id)
                    portfolio.trades.add(trade)
                except Portfolio.DoesNotExist:
                    return Response({'error': 'Portfolio not found'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(trade_serializer.data, status=status.HTTP_201_CREATED)
        return Response(trade_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pk = request.headers.get('Trade-Id')
        trade = self.get_object(pk)
        serializer = TradeSerializer(trade, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.headers.get('Trade-Id')
        trade = self.get_object(pk)
        trade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Trade.objects.get(pk=pk)
        except Trade.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)


class StockAPIView(APIView):

    def get(self, request):
        all_stocks = Stock.objects.all()
        serializer = StockSerializer(all_stocks, many=True)
        return Response({"stocks": serializer.data})

    def post(self, request):
        stock_data = request.data
        serializer = StockSerializer(data=stock_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioAPIView(APIView):

    def get(self, request):
        all_portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(all_portfolios, many=True)
        return Response({'portfolio':serializer.data})

    def post(self, request):
        portfolio_data = request.data
        serializer = PortfolioSerializer(data=portfolio_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
