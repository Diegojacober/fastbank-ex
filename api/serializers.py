from rest_framework import serializers
from core.models import Conta


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['agencia', 'numero']
        read_only_fields = ['agencia', 'numero']


class AccountDetailSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['id', 'saldo', 'created_at']
        read_only_fields = AccountSerializer.Meta.read_only_fields + ['id', 'saldo', 'created_at']
