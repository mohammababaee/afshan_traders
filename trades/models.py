from django.db import models
from jsonschema import ValidationError
import uuid
from users.models import User


class Portfolio(models.Model):
    """
    A user can manage multiple portfolios within their account.
    Each portfolio is identified by a unique name and includes a list of user trades associated with that specific portfolio.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio_name = models.CharField(max_length=30, blank=True)
    portfolio_value = models.FloatField(null=True, blank=True, editable=False)

    def calculate_total_value(self):

        trades = Trade.objects.filter(portfolio=self)

        # Initialize total value
        total_value = 0.0

        for trade in trades:
            if trade.trade_type == "Buy":
                total_value += trade.amount * trade.stock_price
            elif trade.trade_type == "Sell":
                total_value -= trade.amount * trade.stock_price

        return total_value

    def save(self, *args, **kwargs):
        # Calculate and update portfolio value only if there are associated trades
        trades_exist = Trade.objects.filter(portfolio=self).exists()
        if trades_exist:
            total_value = self.calculate_total_value()
            self.portfolio_value = total_value

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Portfolio {self.id}"


class Stock(models.Model):
    """
    Stocks that is curently avaliable in market, At the first phase we just use TSETMC symbols
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=18, primary_key=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Trade(models.Model):
    """
    Eache trade contains detalis about a trade that user have done in their broker

    """

    TRADE_TYPE_CHOICES = [("Buy", "Buy"), ("Sell", "Sell")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trade_date = models.DateField()
    stock_price = models.FloatField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField()
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    portfolio = models.ForeignKey(
        Portfolio, related_name="trades", on_delete=models.CASCADE
    )

    def clean(self):
        if self.stock_price <= 0:
            raise ValidationError("Trade price must be a positive value.")

        if self.amount < 0:
            raise ValidationError("Amount must be a non-negative integer.")

    def save(self, *args, **kwargs):
        # Call the save method of the associated Portfolio
        self.portfolio.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trade_date} - {self.stock.name} - {self.trade_type} - {self.amount} shares at ${self.stock_price} each"
