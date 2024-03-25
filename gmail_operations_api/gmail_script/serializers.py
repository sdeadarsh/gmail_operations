import datetime
from django.apps import apps
from rest_framework import serializers
from django.conf import settings
from django.forms.models import model_to_dict
from gmail_script.models import Mails


class MailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mails
        fields = "__all__"
