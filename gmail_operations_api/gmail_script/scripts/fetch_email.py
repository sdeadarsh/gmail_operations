import datetime

import requests
from django.conf import settings
from gmail_script.token import get_access_token
from gmail_operations_api.utils import error_response, success_response
from gmail_script.helper import email_data, mail_message, check_existing_mail, safe_access, save_all_mail, date_format
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def fetch_message():
    try:
        all_mail_list = list()
        cloud_token = get_access_token()
        if not cloud_token:
            return error_response("token error")
        header = {"Authorization": f'Bearer {cloud_token}', "Content-Type": "application/json"}
        email_id = email_data(header)
        extracted_thread_id, final_db_data = check_existing_mail()
        for email in email_id:
            db_data_dict = dict()
            if email['threadId'] not in extracted_thread_id:
                messages_data = mail_message(email['threadId'], header)
                if messages_data is not None:
                    db_data_dict['mail_id'] = email['id']
                    db_data_dict['thread_id'] = email['threadId']
                    if messages_data['labelIds'][0] != 'UNREAD':
                        db_data_dict['read_status'] = True
                    db_data_dict['mail_tag'] = messages_data['labelIds'][-1]
                    sender_body_path = ['payload', 'headers']
                    sender_result = safe_access(messages_data, sender_body_path)
                    for sender_data in sender_result:
                        if sender_data['name'] == 'Reply-To':
                            db_data_dict['sender'] = sender_data['value']
                        if sender_data['name'] == 'Date':
                            new_data = date_format(sender_data['value'])
                            db_data_dict['mail_datetime'] = datetime.datetime.strptime(new_data[0],
                                                                                       '%a, %d %b %Y %H:%M:%S')
                        if sender_data['name'] == 'Subject':
                            db_data_dict['subject'] = sender_data['value']
                    message_body_path = ['payload', 'parts', 0, 'body', 'data']
                    message_body_result = safe_access(messages_data, message_body_path)
                    if message_body_result is not None:
                        file_name = email['threadId']
                        file_content = message_body_result
                        file_path = f'uploads/{file_name}'
                        default_storage.save(file_path, ContentFile(file_content))
                        db_data_dict['message_body'] = file_name
                        db_data_dict['updated_at'] = datetime.datetime.now()
                        db_data_dict['created_at'] = datetime.datetime.now()
                        print(db_data_dict)
                all_mail_list.append(db_data_dict)
        save_all_mail(all_mail_list)
    except Exception as e:
        error_response("error in script")


def run():
    fetch_message()
