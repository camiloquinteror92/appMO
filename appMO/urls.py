from django.contrib import admin
from django.urls import include
from django.urls import path
from loans.views import (
    CustomerListCreate,
    LoanListCreate,
    PaymentListCreate,
    CustomerLoansList,
    LoanPaymentsList,
    CustomerBalance,
    PaymentCreate,
    DashboardView,  # Corrected import
)

urlpatterns = [
    # Customer related URLs
    path('customers/', CustomerListCreate.as_view(), name='customer-list-create'),
    path('customers/<str:external_id>/balance/', CustomerBalance.as_view(), name='customer-balance'),
    path('customers/<int:customer_id>/loans/', CustomerLoansList.as_view(), name='customer-loans-list'),
    
    # Loan related URLs
    path('loans/', LoanListCreate.as_view(), name='loan-list-create'),
    path('loans/<int:loan_id>/payments/', LoanPaymentsList.as_view(), name='loan-payments-list'),
    
    # Payment related URLs
    path('payments/', PaymentListCreate.as_view(), name='payment-list-create'),
    path('payments/create/', PaymentCreate.as_view(), name='payment-create'),

    path('dashboard/', DashboardView.as_view(), name='dashboard_view'), 
    path('admin/', admin.site.urls),

]
