import random
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
            try:
                portfolio = Portfolio.objects.get(id=portfolio_id)
            except Portfolio.DoesNotExist:
                return Response({'error': 'Portfolio not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            if (portfolio.portfolio_value==None and ((-1 if trade_data['trade_type'] == 'Sell' else 1) * trade_data['amount'] * trade_data['stock_price']) >= 0) or portfolio.portfolio_value + ((-1 if trade_data['trade_type'] == 'Sell' else 1) * trade_data['amount'] * trade_data['stock_price']) >= 0 :
                trade = trade_serializer.save(stock=stock, portfolio=portfolio)
                portfolio.trades.add(trade)
                portfolio.save()
                return Response(trade_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Portfolio value cannot be less than 0 after adding the new trade'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        pk = request.data.get('id')
        trade = self.get_object(pk)
        trade.delete()
        return Response({'message': f'Trade with ID {pk} deleted successfully'}, status=status.HTTP_200_OK)

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

    def delete(self, request):
        pk = request.data.get('symbol')
        stock = self.get_object(pk)
        stock.delete()
        return Response({'message': f'Stock with Name {pk} deleted successfully'}, status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)


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

    def delete(self, request):
        pk = request.data.get('id')
        portfolio = self.get_object(pk)
        portfolio.delete()
        return Response({'message': f'Portfolio with id {pk} deleted successfully'}, status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)


class FetchPortfolioData(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('id')
        portfolio_data = Portfolio.objects.get(id=pk)
        serializer = PortfolioSerializer(portfolio_data, many=False)
        return Response({'portfolio':serializer.data})


class FetchTradeData(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('id')
        trade_data = Trade.objects.get(id=pk)
        serializer = TradeSerializer(trade_data, many=False)
        current_price = serializer.data['amount'] * random.randint(100000, 120000)
        return Response({'trade_information':serializer.data, "trade_current_price":current_price})


class FetchPortfolioInfo(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('id')

        # Retrieve trades efficiently using select_related
        trades = Trade.objects.filter(portfolio_id=pk).select_related('stock')

        serializer = TradeSerializer(trades, many=True)

        # Calculate total value accurately
        total_value = 0
        for item in trades:
            current_price = random.randint(-100000, 120000)
            total_value += (item.amount * current_price) - item.stock_price * item.amount

        # Determine profit status correctly
        is_in_profit = total_value > 0

        return Response({
            'number_of_trades': trades.count(),  # Use trades.count() for efficiency
            'trades': serializer.data,
            'is_in_profit': is_in_profit,
            'current_value': total_value
        })