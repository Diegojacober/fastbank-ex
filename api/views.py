from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication as authenticationJWT
from core.models import Conta
from api import serializers
import random, decimal


class AccountViewSet(viewsets.ModelViewSet):
    # "SELECT * FROM contas";
    queryset = Conta.objects.all()
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Pegar contas para usuários autenticados"""
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
    # "SELECT * FROM contas where user_id = 1";

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AccountDetailSerializer

        return serializers.AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.AccountSerializer(data=request.data)
        if serializer.is_valid():
            agencia = '0001'
            numero = ''
            for n in range(8):
                numero += str(random.randint(0, 9))

            conta = Conta(
                user=self.request.user,
                numero=numero,
                agencia=agencia
            )

            conta.saldo = decimal.Decimal(0)

            conta.save()

            return Response({'message': 'Created'}, status=status.HTTP_201_CREATED)
