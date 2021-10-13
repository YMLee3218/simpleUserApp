from dataclasses import dataclass
from random import randint
from uuid import uuid4

from rest_framework.request import Request
from rest_framework.response import Response

from extend.my_view import MyAPIView
from util.expire_dict import ExpireDict

PHONE_NUMBER = "phone_number"
AUTH_NUMBER = "auth_number"
VERIFICATION_CODE = "verification_code"

AUTHENTICATION_TIME = 300
VERIFICATION_TIME = 600

_sms_authentication: ExpireDict[str, "SMSAuthenticationData"] = ExpireDict(AUTHENTICATION_TIME, 300)


@dataclass
class SMSAuthenticationData:
    auth_number: int
    verification_code: str

    @staticmethod
    def create() -> "SMSAuthenticationData":
        return SMSAuthenticationData(randint(10000, 100000), str(uuid4()))


class SMSAuthenticationSendingView(MyAPIView):
    def post(self, request: Request) -> Response:
        phone_number: str = request.data[PHONE_NUMBER]

        authentication_data: SMSAuthenticationData = SMSAuthenticationData.create()
        _sms_authentication[phone_number] = authentication_data
        return Response({AUTH_NUMBER: authentication_data.auth_number})

