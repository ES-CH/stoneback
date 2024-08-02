from rest_framework import serializers

from apps.accounting.models import Accounting


class AccountingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounting
        fields = '__all__'
