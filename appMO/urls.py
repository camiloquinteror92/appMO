from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from loans.views import (
    CustomerListCreate,
    LoanListCreate,
    PaymentListCreate,
    CustomerLoansList,
    LoanPaymentsList,
    CustomerBalance,
    PaymentCreate,
    DashboardView,
)

# Configuration for drf-yasg (Swagger & Redoc)
schema_view = get_schema_view(
    openapi.Info(
        title="AppMO API",
        default_version='v1',
        description="API documentation for AppMO",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="contact@yourwebsite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Customer related URLs
customer_patterns = [
    path('customers/', CustomerListCreate.as_view(), name='customer-list-create'),
    path('customers/<str:external_id>/balance/', CustomerBalance.as_view(), name='customer-balance'),
    path('customers/<int:customer_id>/loans/', CustomerLoansList.as_view(), name='customer-loans-list'),
]

# Loan related URLs
loan_patterns = [
    path('loans/', LoanListCreate.as_view(), name='loan-list-create'),
    path('loans/<int:loan_id>/payments/', LoanPaymentsList.as_view(), name='loan-payments-list'),
]

# Payment related URLs
payment_patterns = [
    path('payments/', PaymentListCreate.as_view(), name='payment-list-create'),
    path('payments/create/', PaymentCreate.as_view(), name='payment-create'),
]

# General, administrative and documentation URLs
general_patterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = customer_patterns + loan_patterns + payment_patterns + general_patterns
