from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.http import JsonResponse
from gmail_script.helper import email_data, mail_message, check_existing_mail, save_all_mail
from gmail_script.token import get_access_token
from gmail_script.scripts.fetch_email import fetch_message


class FetchMessageTestCase(TestCase):

    @patch('gmail_script.helper.get_access_token')
    @patch('gmail_script.helper.email_data')
    @patch('gmail_script.helper.mail_message')
    @patch('gmail_script.helper.check_existing_mail')
    @patch('gmail_script.helper.save_all_mail')
    def test_fetch_message_success(self, mock_save_all_mail, mock_check_existing_mail, mock_mail_message,
                                   mock_email_data, mock_get_access_token):
        # Mocking the dependencies
        mock_get_access_token.return_value = 'dummy_token'
        mock_email_data.return_value = [{'id': 5, 'threadId': '18e4a07ae13b8489'},
                                        {'id': 6, 'threadId': '18e4a07ae13b8489'}]
        mock_check_existing_mail.return_value = (['18e4a07ae13b8489'], [{'thread_id': '18e4a07ae13b8489', 'id': 6}])
        mock_mail_message.return_value = {
            'labelIds': ['inbox'],
            'payload': {
                'headers': [
                    {'name': 'Reply-To', 'value': 'sender@example.com'},
                    {'name': 'Date', 'value': 'Sun, 17 Mar 2024 01:30:00 +0000'},
                    {'name': 'Subject', 'value': 'Test Subject'},
                ],
                'parts': [{'body': {'data': 'SGVsbG8gd29ybGQh'}, 'mimeType': 'text/plain'}]
            }
        }

        # Calling the function
        response = fetch_message()

        # Assertions
        self.assertEqual(response.status_code, 200)
        mock_save_all_mail.assert_called_once_with([
            {
                "id": 5,
                "mail_id": "18e4a07ae13b8489",
                "thread_id": "18e4a07ae13b8489",
                "message_body": "18e4a07ae13b8489",
                "sender": "noreply@medium.com",
                "mail_datetime": "2024-03-17T01:30:00Z",
                "subject": "How AWS Rekognition Helps Protect Childhood | Manuel E. de Paz Carmona in AWS in Plain English",
                "read_status": False,
                "mail_tag": "inbox",
                "updated_at": "2024-03-24T06:54:28.925595Z",
                "created_at": "2024-03-24T06:54:28.925601Z",
                "is_active": True
            },
            {
                "id": 6,
                "mail_id": "18e46427f468cbb1",
                "thread_id": "18e4a07ae13b8489",
                "message_body": "18e46427f468cbb1",
                "sender": "",
                "mail_datetime": "2024-03-16T07:55:46Z",
                "subject": "What is the salary of an entry level scientist at BARC?",
                "read_status": False,
                "mail_tag": "inbox",
                "updated_at": "2024-03-24T06:54:28.925630Z",
                "created_at": "2024-03-24T06:54:28.925636Z",
                "is_active": True
            },
            {
                "id": 7,
                "mail_id": "18e38b51fd26e987",
                "thread_id": "18e38b51fd26e987",
                "message_body": "18e38b51fd26e987",
                "sender": "Adobe Express <mail@email.adobe.com>",
                "mail_datetime": "2024-03-13T09:46:11Z",
                "subject": "Convert your videos to GIFS for free",
                "read_status": False,
                "mail_tag": "inbox",
                "updated_at": "2024-03-24T06:54:28.925664Z",
                "created_at": "2024-03-24T06:54:28.925670Z",
                "is_active": True
            }
        ])
