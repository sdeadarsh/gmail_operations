import pandas as pd
import requests
from django.conf import settings
from gmail_operations_api.utils import error_response, success_response
from gmail_script.models import Mails
import numpy as np
from dateutil import parser


def email_data(header):
    response = requests.get(url=f"{settings.EMAIL_URL}", headers=header)
    if response.status_code != 200:
        return error_response("No Data Found")
    email_id = response.json()['messages']
    return email_id


def mail_message(thread_id, header):
    message_data = None
    try:
        response = requests.get(url=f"{settings.EMAIL_URL}/{thread_id}", headers=header)
        if response.status_code != 200:
            return error_response("No Data Found")
        message_data = response.json()
        return message_data
    except:
        return message_data


def check_existing_mail():
    db_mail_id = pd.DataFrame(Mails.objects.all().values('thread_id', 'id'))
    df = db_mail_id.replace({np.nan: None})
    if df.empty:
        return error_response("No Data Found")
    final_data = df.to_dict(orient="records")
    extracted_email_ids = [d['thread_id'] for d in final_data]
    return extracted_email_ids, final_data


def safe_access(data, path):
    try:
        for key in path:
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return None


def save_all_mail(all_mail_list):
    mail_list = [Mails(**vals) for vals in all_mail_list]
    Mails.objects.bulk_create(mail_list)


def update_all_mail(all_mail_list):
    # mail_list = [Mails(**vals) for vals in all_mail_list]
    fields = ['mail_id', 'thread_id', 'read_status', 'mail_tag', 'subject', 'mail_datetime', 'message_body',
              'updated_at']
    Mails.objects.bulk_update(all_mail_list, fields)
    print('done')


def date_format(date_strings):
    parsed_dates = [parser.parse(date_strings)]

    # Convert parsed dates to the desired format
    desired_format = "%a, %d %b %Y %H:%M:%S"
    formatted_dates = [date.strftime(desired_format) for date in parsed_dates]
    return formatted_dates
