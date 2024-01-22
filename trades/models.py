from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=18)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Trade(models.Model):
    TRADE_TYPE_CHOICES = [("Buy", 'Buy'), ("Sell", "Sell")]

    trade_date = models.DateField()
    trade_price = models.FloatField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField()
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.trade_date} - {self.stock.name} - {self.get_trade_type_display()} - {self.amount} shares at ${self.trade_price} each"


class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length=30, blank=True)
    trades = models.ManyToManyField(Trade, blank=True)

    def __str__(self):
        return f"Portfolio {self.id}"
