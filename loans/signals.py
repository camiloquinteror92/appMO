from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Payment, Loan

@receiver(post_save, sender=Payment)
def update_loan_balance(sender, instance, **kwargs):
    """Update the outstanding amount of the associated loan after saving a Payment."""
    loan = instance.loan
    loan.recalculate_balance()
