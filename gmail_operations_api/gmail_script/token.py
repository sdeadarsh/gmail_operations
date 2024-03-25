import requests
from django.conf import settings


def get_access_token():
    cloud_token = None
    try:
        url = settings.REFRESH_TOKEN_URL
        data = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'refresh_token': settings.REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            cloud_token = response.json()['access_token']
            return cloud_token
    except Exception as e:
        return cloud_token
