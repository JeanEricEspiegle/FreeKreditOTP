import datetime
import math
import random

import requests

CLIENT_ID = ''
CLIENT_SECRET = ''


class OTPVerification:
    token = ''
    otp = ''
    otp_created_time = None
    token_created_time = None

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = "https://sms.360.my/oauth/token"

        payload = {'client_id': 'QJ0dNxzaLO',
                   'client_secret': 'OIchiBSNTuLb9DefnHXlCra5w5J5PHQgqcp8UzLq',
                   'grant_type': 'client_credentials'}
        files = [

        ]
        headers = {'Accept': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        self.token_created_time = datetime.datetime.now()
        return response.json()['access_token']

    def generate_otp(self, number):

        if (datetime.datetime.now() - self.token_created_time).total_seconds() >= 3600:
            self.token = self.get_token()

        url = "https://sms.360.my/api/bulk360/v2.0"

        digits = "0123456789"
        self.otp = ''.join([digits[math.floor(random.random() * 10)] for _ in range(6)])

        payload = {'to': number,
                   'text': f"Hangtuah Club OTP - {self.otp}",
                   'detail': '1'}
        headers = {
            'Authorization': f"Bearer {self.token}",
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.otp_created_time = datetime.datetime.now()

    def check_otp(self, otp_user_input):
        if (datetime.datetime.now() - self.otp_created_time).total_seconds() >= 300:
            return 'timeout'
        if str(otp_user_input) != self.otp:
            return 'fail'

        self.otp = '0'
        self.otp_created_time = None
        return 'success'

    def checktime(self):
        if self.otp_created_time == None:
            return 100
        elif (datetime.datetime.now() - self.otp_created_time).total_seconds() >= 180:
            print((datetime.datetime.now() - self.otp_created_time).total_seconds())
            self.otp_created_time = None
            return 0
        else:
            print((datetime.datetime.now() - self.otp_created_time).total_seconds())
            return 1
