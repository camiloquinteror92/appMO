from rest_framework import serializers
from .models import Customer, Loan, Payment
import datetime

class CustomerSerializer(serializers.ModelSerializer):
    total_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def validate_date_of_birth(self, value):
        if value > (datetime.date.today() - datetime.timedelta(days=18 * 365)):
            raise serializers.ValidationError("El cliente debe ser mayor de edad.")
        return value


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, data):
        customer = data.get("customer")
        if customer.score <= 60:
            raise serializers.ValidationError("El cliente debe tener un score superior a 60 para obtener un préstamo.")
        
        # Checking if the sum of the new loan and the customer's existing debt exceeds the customer's score.
        if data.get("amount") + customer.total_debt > customer.score:
            raise serializers.ValidationError(f"La suma del nuevo préstamo y la deuda existente del cliente no debe exceder su score de {customer.score}.")
        
        max_loan_amount = customer.score
        if data.get("amount") > max_loan_amount:
            raise serializers.ValidationError(f"El monto del préstamo no puede exceder {max_loan_amount}.")
        
        return data        

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Loan amount must be positive.")
        return value
class PaymentSerializer(serializers.ModelSerializer):
    loan_external_id = serializers.CharField(source='loan.external_id', read_only=True)
    customer_external_id = serializers.CharField(source='customer.external_id', read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        loan = data['loan']
        if Payment.objects.filter(loan=loan, created_at__date=datetime.date.today()).exists():
            raise serializers.ValidationError("Ya existe un pago para este préstamo hoy.")
        
        # Checking if the payment amount exceeds the outstanding amount of the loan.
        if data.get("total_amount") > loan.outstanding:
            raise serializers.ValidationError(f"El monto del pago no puede exceder el monto pendiente del préstamo de {loan.outstanding}.")
        
        return data
    

class CustomerBalanceSerializer(serializers.ModelSerializer):
    total_debt = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    available_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Customer
        fields = ('external_id', 'score', 'total_debt', 'available_amount')