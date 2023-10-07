from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Case, When, F, DecimalField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Customer, Loan, Payment
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from django.db import transaction
from .serializers import (
    CustomerSerializer,
    LoanSerializer,
    PaymentSerializer,
    CustomerBalanceSerializer,
)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        # Gathering general information
        total_customers = Customer.objects.count()
        total_loans = Loan.objects.count()
        total_payments = Payment.objects.count()

        # Getting a list of customers (for simplicity, we will limit to 10 for now)
        customers = Customer.objects.all()[:10]

        # Getting a list of loans (limiting to 10 for now)
        loans = Loan.objects.all()[:10]

        # Calculating total balance (sum of all customer balances)
        total_balance = sum(customer.total_balance for customer in Customer.objects.all())

        # Getting the top customers (sorting by total_debt in descending order)
        top_customers = Customer.objects.annotate(
            annotated_total_debt=Sum(
                Case(
                    When(loans__status=Loan.ACCEPTED, then=F('loans__outstanding')),
                    default=0, output_field=DecimalField()
                )
            )
        ).order_by('-annotated_total_debt')[:10]


        # Getting the recent loans (sorting by taken_at in descending order)
        recent_loans = Loan.objects.filter(status=Loan.ACCEPTED).order_by('-taken_at')[:10]

        context = {
            'total_customers': total_customers,
            'total_loans': total_loans,
            'total_payments': total_payments,
            'customers': customers,
            'loans': loans,
            'total_balance': total_balance,
            'top_customers': top_customers,
            'recent_loans': recent_loans,
        }

        return render(request, 'dashboard.html', context)



class PaymentCreate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Obtener los nombres de los clientes con préstamos activos
        active_customers = Customer.objects.filter(loans__status=Loan.ACCEPTED).distinct()
        customer_serializer = CustomerSerializer(active_customers, many=True)
        return Response({"active_customers": customer_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            loan = serializer.validated_data['loan']
            loan.recalculate_balance()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoanListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class PaymentListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CustomerLoansList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Loan.objects.filter(customer_id=customer_id)


class LoanPaymentsList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return Payment.objects.filter(loan_id=loan_id)


class CustomerBalance(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerBalanceSerializer
    lookup_field = 'external_id'


class CreateCustomer(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['status'] = Customer.ACTIVE  # Set status to Active
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCustomerBalance(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, pk=customer_id)
        loans = Loan.objects.filter(customer=customer)
        total_loaned = sum(loan.amount for loan in loans)
        total_paid = sum(payment.total_amount for loan in loans for payment in loan.payments.filter(status=Payment.ACCEPTED))
        available_amount = customer.score - total_loaned
        response_data = {
            "external_id": customer.external_id,
            "score": customer.score,
            "available_amount": available_amount,
            "total_debt": total_loaned,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CreateLoan(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['status'] = Loan.ACCEPTED  # Set status to Active
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetLoansByCustomer(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Loan.objects.filter(customer_id=customer_id)



class CreatePayment(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.validated_data['loan']
            if loan.apply_payment(serializer.validated_data['total_amount']):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Payment amount exceeds outstanding debt."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetPaymentsByCustomer(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, pk=customer_id)
        payments = Payment.objects.filter(customer=customer)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
