# apps/wallet/urls.py
from django.urls import path
from .views import FundWalletView, TransactionListView, WalletView

urlpatterns = [
    path("", WalletView.as_view()),
    path('fund/', FundWalletView.as_view()),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
]
