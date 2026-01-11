from decimal import Decimal
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from wallet.models import Wallet, Transaction
from .models import Tricycle, Investment
from .serializers import InvestSerializer
import uuid


class InvestView(GenericAPIView):
    serializer_class = InvestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        wallet = Wallet.objects.get(user=user)

        tricycle = Tricycle.objects.get(id=serializer.validated_data["tricycle_id"])
        investment_type = serializer.validated_data["investment_type"]
        amount = serializer.validated_data["amount"]

        if wallet.balance < amount:
            return Response(
                {"detail": "Insufficient wallet balance"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            if investment_type == "full":
                if amount != tricycle.total_value:
                    return Response(
                        {"detail": "Full ownership requires full tricycle value"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                ownership = Decimal("100.00")

            else:  # shared
                ownership = (amount / tricycle.total_value) * Decimal("100")

                total_owned = Investment.objects.filter(
                    tricycle=tricycle
                ).aggregate(
                    total=models.Sum("ownership_percentage")
                )["total"] or Decimal("0")

                if total_owned + ownership > 100:
                    return Response(
                        {"detail": "Not enough shares available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            Investment.objects.create(
                user=user,
                tricycle=tricycle,
                investment_type=investment_type,
                amount_invested=amount,
                ownership_percentage=ownership
            )

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="debit",
                reference=str(uuid.uuid4()),
                description="Tricycle investment"
            )

            wallet.balance -= amount
            wallet.save()

        return Response(
            {"message": "Investment successful"},
            status=status.HTTP_201_CREATED
        )

