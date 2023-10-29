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

from rest_framework.decorators import action


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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_path='sacar')
    def sacar(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first()
        
        serializer_recebido = serializers.SaqueSerializer(data=request.data)
        
        if serializer_recebido.is_valid() and conta:
            valor_saque = decimal.Decimal(serializer_recebido.validated_data.get('value'))
            saldo = decimal.Decimal(conta.saldo)
            
            comparacao = saldo.compare(valor_saque)
            
            if comparacao == 0 or comparacao == 1:
                novo_valor = 0 if saldo - valor_saque <= 0 else  saldo - valor_saque
                
                conta.saldo = novo_valor
                
                conta.save()
                
                return Response({"saldo": conta.saldo}, status=status.HTTP_200_OK)
            
            return Response({'message': 'Saldo insuficiente'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['POST'], detail=True, url_path='depositar')
    def depositar(self, request, pk=None):
        conta = Conta.objects.filter(id=pk).first()
        serializer_recebido = serializers.DepositoSerializer(data=request.data)
        
        if serializer_recebido.is_valid() and conta:
            valor_deposito = decimal.Decimal(serializer_recebido.validated_data.get('value'))
            saldo = decimal.Decimal(conta.saldo)
            
            conta.saldo = saldo + valor_deposito
            conta.save()
            
            return Response({"saldo": conta.saldo}, status=status.HTTP_200_OK)
        
        return Response(serializer_recebido.errors, status=status.HTTP_400_BAD_REQUEST)
