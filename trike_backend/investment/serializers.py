from rest_framework import serializers

class InvestSerializer(serializers.Serializer):
    tricycle_id = serializers.IntegerField()
    investment_type = serializers.ChoiceField(choices=["full", "share"])
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
