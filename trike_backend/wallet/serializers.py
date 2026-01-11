# wallet/serializers.py
from rest_framework import serializers
from .models import Wallet, Transaction
from .services import usdt_to_local

class WalletSerializer(serializers.ModelSerializer):
    balance_usdt = serializers.SerializerMethodField()
    balance_local = serializers.SerializerMethodField()
    local_currency = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = (
            "balance_usdt",
            "balance_local",
            "local_currency",
        )

    def get_balance_usdt(self, obj):
        return obj.balance

    def get_balance_local(self, obj):
        return usdt_to_local(obj.balance)

    def get_local_currency(self, obj):
        return "NGN"


class FundWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "transaction_type",
            "reference",
            "description",
            "created_at",
        ]