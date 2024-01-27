from django.db import models
from django.contrib.auth import get_user_model
from apps.advertisement.models import Advertisement


class Payment(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        related_name='user_payments',
        verbose_name='User',
        null=True
    )

    amount  = models.IntegerField(
        verbose_name='Amount : ﷼',
        default=0
    )

    created = models.DateTimeField(
        verbose_name='Date Created Payment',
        null=True,
        blank=True,
        auto_now_add=True,
    )

    is_paid = models.BooleanField(
        verbose_name='Is Paid ?',
        null=True,
        blank=True,
        default=False
    )

    getway = models.CharField(
        max_length=70,
        verbose_name="Getway Name",
        null=True,
        blank=True,
        default="zarinpal"
    )

    transaction_id = models.CharField(
        max_length=70,
        verbose_name="Transaction Id",
        null=True,
        blank=True,
    )
    
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.PROTECT,
        related_name="advertisement_payments",
        null=True,
        blank=True
    )
    
    def __str__(self):
        return str(self.advertisement.id)

