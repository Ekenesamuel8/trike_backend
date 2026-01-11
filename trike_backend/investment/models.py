from django.db import models
from django.conf import settings


class Tricycle(models.Model):
    name = models.CharField(max_length=100)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Investment(models.Model):
    INVESTMENT_TYPE = (
        ("full", "Full Ownership"),
        ("share", "Shared Ownership"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tricycle = models.ForeignKey(Tricycle, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=10, choices=INVESTMENT_TYPE)

    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    ownership_percentage = models.DecimalField(
            max_digits=5,
            decimal_places=2,
            editable=False
        )
    created_at = models.DateTimeField(auto_now_add=True)
