from django.db import models, transaction
from decimal import Decimal
from django.core.validators import MinValueValidator
from rest_framework import serializers
import logging

# Configuración del logger
logger = logging.getLogger(__name__)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    external_id = models.CharField(max_length=255, unique=True)
    score = models.PositiveIntegerField()

    ACTIVE = 1
    INACTIVE = 2
    STATUS_CHOICES = [
        (ACTIVE, 'Activo'),
        (INACTIVE, 'Inactivo'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    @property
    def total_balance(self):
        accepted_status = Loan.ACCEPTED
        total_loaned = sum(loan.amount for loan in self.loans.all() if loan.status == accepted_status)
        total_paid = sum(payment.total_amount for loan in self.loans.all() for payment in loan.payments.filter(status=Payment.ACCEPTED))
        balance = total_loaned - total_paid
        return balance

    @property
    def total_debt(self):
        # Filtrando los préstamos del cliente con estado PENDING o ACCEPTED
        relevant_loans = self.loans.filter(status__in=[Loan.PENDING, Loan.ACCEPTED])
        # Sumando el 'outstanding' de todos estos préstamos para obtener la deuda total
        total_debt_value = sum(loan.outstanding for loan in relevant_loans)
        logger.info(f"Calculando deuda total para el cliente {self.id}. Préstamos relevantes: {[loan.id for loan in relevant_loans]}. Deuda total: {total_debt_value}")
        return total_debt_value


    @property
    def available_amount(self):
        return self.score - self.total_debt


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    external_id = models.CharField(max_length=255, unique=True)
    contract_version = models.TextField(null=True, blank=True)

    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    PAID = 4
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (PAID, 'Paid'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2)
    taken_at = models.DateTimeField(null=True, blank=True)

    @property
    def balance(self):
        total_accepted_payments = sum(payment.amount for payment in self.payments.filter(status=Payment.ACCEPTED))
        balance = self.amount - Decimal(total_accepted_payments)
        return balance

    def recalculate_balance(self):
        total_accepted_payments = sum(payment.total_amount for payment in self.payments.filter(status=Payment.ACCEPTED))
        self.outstanding = self.amount - Decimal(total_accepted_payments)
        if self.outstanding == 0:
            self.status = Loan.PAID
        else:
            self.status = Loan.ACCEPTED
        self.save()
    
    def mark_as_paid(self):
        if self.outstanding == Decimal('0'):
            self.status = Loan.PAID
            self.save()

    @transaction.atomic
    def apply_payment(self, payment_amount):
        """Apply a payment to the loan. Update the outstanding amount and possibly change the loan's status."""
        logger.info(f"Aplicando pago de {payment_amount} a préstamo con saldo pendiente inicial: {self.outstanding}")
        if payment_amount <= self.outstanding:
            self.outstanding -= payment_amount
            if self.outstanding == 0:
                self.status = Loan.PAID
            else:
                self.status = Loan.ACCEPTED
            self.save()
            logger.info(f"Pago aplicado. Nuevo saldo pendiente para el préstamo: {self.outstanding}")
            return True
        logger.warning(f"El pago de {payment_amount} excede el saldo pendiente de {self.outstanding}. Pago no aplicado.")
        return False   

class Payment(models.Model):
    external_id = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')

    PROCESSING = 1
    ACCEPTED = 2
    REJECTED = 3
    STATUS_CHOICES = [
        (PROCESSING, 'Processing'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=PROCESSING)
    created_at = models.DateTimeField(auto_now_add=True)

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    @classmethod
    def get_loans_by_customer(cls, customer):
        return cls.objects.filter(customer=customer)
