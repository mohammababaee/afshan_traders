from django.db import models
from jsonschema import ValidationError


class Portfolio(models.Model):
    '''
    A user can manage multiple portfolios within their account.
    Each portfolio is identified by a unique name and includes a list of user trades associated with that specific portfolio.
    '''
    portfolio_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Portfolio {self.id}"


class Stock(models.Model):
    '''
    Stocks that is curently avaliable in market, At the first phase we just use TSETMC symbols
    '''
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=18, primary_key=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Trade(models.Model):
    '''
    Eache trade contains detalis about a trade that user have done in their broker
    
    '''
    TRADE_TYPE_CHOICES = [("Buy", 'Buy'), ("Sell", "Sell")]

    trade_date = models.DateField()
    stock_price = models.FloatField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField()
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    portfolio = models.ForeignKey(Portfolio, related_name='trades', on_delete=models.CASCADE)

    def clean(self):
        if self.stock_price <= 0:
            raise ValidationError("Trade price must be a positive value.")

        if self.amount < 0:
            raise ValidationError("Amount must be a non-negative integer.")

    def __str__(self):
        return f"{self.trade_date} - {self.stock.name} - {self.get_trade_type_display()} - {self.amount} shares at ${self.stock_price} each"

