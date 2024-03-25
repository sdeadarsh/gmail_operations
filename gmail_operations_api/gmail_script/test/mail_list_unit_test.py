from unittest import TestCase, mock
from gmail_script.views import MailsViewSet
from django.http import JsonResponse
from gmail_script.models import Mails


class TestListView(TestCase):

    @mock.patch('Mails.objects.all().values')
    def test_successful_response_with_data(self, mock_values):
        # Sample data
        mock_values.return_value = [{
            "id": 6,
            "mail_id": "18e46427f468cbb1",
            "thread_id": "18e46427f468cbb1",
            "message_body": "18e46427f468cbb1",
            "sender": "",
            "mail_datetime": "2024-03-16T07:55:46Z",
            "subject": "What is the salary of an entry level scientist at BARC?",
            "read_status": False,
            "mail_tag": "inbox",
            "updated_at": "2024-03-24T06:54:28.925630Z",
            "created_at": "2024-03-24T06:54:28.925636Z",
            "is_active": True
        }]

        # Mock request
        request = mock.Mock()

        # Call the function
        view = MailsViewSet()
        response = view.list(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the response data

    @mock.patch('Mails.objects.all().values')
    def test_successful_response_with_empty_data(self, mock_values):
        # Empty data
        mock_values.return_value = []

        # Mock request
        request = mock.Mock()

        # Call the function
        view = MailsViewSet()
        response = view.list(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "No Data Found")

    @mock.patch('Mails.objects.all().values')
    def test_error_response(self, mock_values):
        # Simulate exception
        mock_values.side_effect = Exception("Test Exception")

        # Mock request
        request = mock.Mock()

        # Call the function
        view = MailsViewSet()
        response = view.list(request)

        # Assertions
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data['message'], "Error in Mails")
