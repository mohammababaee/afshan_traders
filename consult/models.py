from django.db import models
from trades.models import Portfolio
from users.models import User


class Consult(models.Model):
    STATUS_CHOICES = (
        ("p", "Pending"),
        ("a", "Accepted"),
        ("r", "Rejected"),
        ("e", "Expired"),
        ("d", "Done"),
    )

    requested_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requested_consults",
        null=False,
        blank=False,
    )
    related_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=False, blank=False
    )
    status = models.CharField(
        choices=STATUS_CHOICES, default="p", max_length=1, null=False, blank=False
    )
    consultant = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="consultant_consults",
        null=False,
        blank=False,
    )
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Consultation for {self.related_portfolio} by {self.consultant}"
