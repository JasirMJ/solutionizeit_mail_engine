from mail_configuration.models import MailRecord
from rest_framework import serializers


class MailRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailRecord
        fields = '__all__'
