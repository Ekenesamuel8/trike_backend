# apps/wallet/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import WalletSerializer
from .models import Wallet

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(
            user=request.user
        )
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
