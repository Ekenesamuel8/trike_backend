# apps/wallet/views.py
import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Wallet, Transaction
from .serializers import FundWalletSerializer, WalletSerializer, TransactionSerializer
from .services import ngn_to_usdt

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(
            user=request.user
        )
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    
class FundWalletView(GenericAPIView):
    serializer_class = FundWalletSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FundWalletSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount_ngn = serializer.validated_data["amount"]
        amount_usdt = ngn_to_usdt(amount_ngn)

        wallet = Wallet.objects.get(user=request.user)

        with transaction.atomic():
            # create transaction record
            Transaction.objects.create(
                wallet=wallet,
                amount=amount_usdt,
                transaction_type="credit",
                reference=str(uuid.uuid4()),
                description="Wallet funding"
            )

            # update wallet balance
            wallet.balance += amount_usdt
            wallet.save()

        return Response({
            "message": "Wallet funded successfully",
            "amount_usdt": amount_usdt,
            "balance": wallet.balance
        }, status=status.HTTP_200_OK)
    
class TransactionListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            wallet__user=self.request.user
        ).order_by("-created_at")
