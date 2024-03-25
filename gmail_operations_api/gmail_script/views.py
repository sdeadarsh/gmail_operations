import datetime
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, views
from gmail_script.serializers import MailsSerializer
from gmail_script.models import Mails
import pandas as pd
import numpy as np
from gmail_script.scripts.fetch_email import fetch_message
from rest_framework.decorators import action
from gmail_script.token import get_access_token
from gmail_operations_api.utils import error_response, success_response
from gmail_script.helper import email_data, mail_message, check_existing_mail, safe_access, update_all_mail, date_format
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# Create your views here.


class MailsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = MailsSerializer
    queryset = Mails.objects.filter()

    def list(self, request, *args, **kwargs):
        try:
            df_data = pd.DataFrame(Mails.objects.all().values())
            df = df_data.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            final_data = df.to_dict(orient="records")
            return success_response(final_data)
        except Exception as e:
            return error_response('Error in Mails')

    def retrieve(self, request, *args, **kwargs):
        response = super(MailsViewSet, self).retrieve(request, *args, **kwargs)
        return success_response(response.data)

    def destroy(self, request, *args, **kwargs):
        Mails.objects.filter(pk=kwargs['pk']).update(is_active=0)
        return success_response("successfully deleted")

    def create(self, request, *args, **kwargs):
        fetch_message()
        return success_response("All mails successfully fetched from gmail")

    def update(self, request, *args, **kwargs):
        try:
            response = super(MailsViewSet, self).update(request, *args, **kwargs)
            return response
        except Exception as e:
            return error_response("error in update")

    @action(methods=['GET'], detail=False)
    def update_mails(self, request, *args, **kwargs):
        try:
            all_mail_list = list()
            cloud_token = get_access_token()
            if not cloud_token:
                return error_response("token error")
            header = {"Authorization": f'Bearer {cloud_token}', "Content-Type": "application/json"}
            email_id = email_data(header)
            extracted_thread_id, final_db_data = check_existing_mail()
            for email, db_entry in zip(email_id, final_db_data):
                thread_id = email['threadId']
                if thread_id in extracted_thread_id:
                    mail_instance = Mails(id=db_entry['id'])
                    messages_data = mail_message(email['threadId'], header)
                    if messages_data is not None:
                        mail_instance.mail_id = email['id']
                        mail_instance.thread_id = email['threadId']
                        if messages_data['labelIds'][0] != 'UNREAD':
                            mail_instance.read_status = True
                        mail_instance.mail_tag = messages_data['labelIds'][-1]
                        sender_body_path = ['payload', 'headers']
                        sender_result = safe_access(messages_data, sender_body_path)
                        for sender_data in sender_result:
                            if sender_data['name'] == 'Reply-To':
                                mail_instance.sender = sender_data['value']
                            if sender_data['name'] == 'Date':
                                new_data = date_format(sender_data['value'])
                                mail_instance.mail_datetime = datetime.datetime.strptime(new_data[0],
                                                                                           '%a, %d %b %Y %H:%M:%S')
                            if sender_data['name'] == 'Subject':
                                mail_instance.subject = sender_data['value']
                        message_body_path = ['payload', 'parts', 0, 'body', 'data']
                        message_body_result = safe_access(messages_data, message_body_path)
                        if message_body_result is not None:
                            file_name = email['threadId']
                            file_content = message_body_result
                            file_path = f'uploads/{file_name}'
                            default_storage.save(file_path, ContentFile(file_content))
                            mail_instance.message_body = file_name
                            mail_instance.updated_at = datetime.datetime.now()
                    all_mail_list.append(mail_instance)
                    break
            update_all_mail(all_mail_list)
            return success_response("All mails updated successfully")
        except Exception as e:
            return error_response("error in updating the existing mails")
