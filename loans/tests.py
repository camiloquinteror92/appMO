
from django.test import TestCase
from .models import Customer, Loan, Payment
from .serializers import CustomerSerializer, LoanSerializer, PaymentSerializer
from decimal import Decimal

class CustomerModelTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth="1990-01-01",
            external_id="123456",
            score=100
        )

    def test_total_balance_calculation(self):
        # Setup: Create associated loans and payments
        # Note: This is a simple example, more detailed scenarios should be tested
        Loan.objects.create(customer=self.customer, amount=Decimal('50.0'), outstanding=Decimal('25.0'))
        # Assert
        self.assertEqual(self.customer.total_balance, Decimal('25.0'))

    def test_total_debt_calculation(self):
        # Setup: Create associated loans
        Loan.objects.create(customer=self.customer, amount=Decimal('50.0'), outstanding=Decimal('50.0'))
        # Assert
        self.assertEqual(self.customer.total_debt, Decimal('50.0'))
        
    def test_available_amount_calculation(self):
        # Assert
        self.assertEqual(self.customer.available_amount, self.customer.score - self.customer.total_debt)


class LoanModelTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth="1990-01-01",
            external_id="123456",
            score=100
        )
        self.loan = Loan.objects.create(customer=self.customer, amount=Decimal('50.0'), outstanding=Decimal('50.0'))

    def test_mark_as_paid(self):
        # Setup: Set outstanding to 0
        self.loan.outstanding = Decimal('0.0')
        # Act
        self.loan.mark_as_paid()
        # Assert
        self.assertEqual(self.loan.status, Loan.PAID)

    def test_apply_payment(self):
        initial_outstanding = self.loan.outstanding
        payment_amount = Decimal('25.0')
        # Act
        self.loan.apply_payment(payment_amount)
        # Assert
        self.assertEqual(self.loan.outstanding, initial_outstanding - payment_amount)


class CustomerSerializerTests(TestCase):

    def test_validate_date_of_birth(self):
        # Test data: underage customer
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "date_of_birth": "2010-01-01",  # This date will make the customer underage
            "external_id": "123456",
            "score": 100
        }
        serializer = CustomerSerializer(data=data)
        # Assert that validation fails for underage customers
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_of_birth", serializer.errors)


class LoanSerializerTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth="1990-01-01",
            external_id="123456",
            score=100
        )

    def test_validate_customer_score(self):
        # Test data with a low score customer
        low_score_customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            date_of_birth="1990-01-01",
            external_id="654321",
            score=50
        )
        data = {
            "customer": low_score_customer.id,
            "amount": Decimal('25.0')
        }
        serializer = LoanSerializer(data=data)
        # Assert validation behavior based on customer score
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_validate_loan_amount(self):
        # Test data with loan amount exceeding customer's score
        data = {
            "customer": self.customer.id,
            "amount": Decimal('150.0')  # This amount will exceed the customer's score
        }
        serializer = LoanSerializer(data=data)
        # Assert validation behavior based on loan amount and customer's score
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class PaymentSerializerTests(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth="1990-01-01",
            external_id="123456",
            score=100
        )
        self.loan = Loan.objects.create(customer=self.customer, amount=Decimal('50.0'), outstanding=Decimal('50.0'))

    def test_validate_existing_payment_today(self):
        # Test data with a payment made today for the loan
        Payment.objects.create(loan=self.loan, customer=self.customer, total_amount=Decimal('25.0'))
        data = {
            "loan": self.loan.id,
            "customer": self.customer.id,
            "total_amount": Decimal('25.0')
        }
        serializer = PaymentSerializer(data=data)
        # Assert validation behavior based on existing payments for the day
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_validate_payment_exceeding_outstanding(self):
        # Test data with payment amount exceeding the loan's outstanding
        data = {
            "loan": self.loan.id,
            "customer": self.customer.id,
            "total_amount": Decimal('60.0')  # This amount will exceed the loan's outstanding
        }
        serializer = PaymentSerializer(data=data)
        # Assert validation behavior based on payment amount and loan's outstanding amount
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

