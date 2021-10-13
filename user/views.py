from uuid import uuid1

from django.contrib.auth.models import User
from django.forms.fields import EmailField, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response

from extend.my_view import MyAPIView
from sms_auth.views import VERIFICATION_CODE, is_verification_valid, remove_verification
from .models import Profile

EMAIL = "email"
NICKNAME = "nickname"
PASSWORD = "password"
NAME = "name"
PHONE_NUMBER = "phone_number"
TOKEN = "token"


class UserView(MyAPIView):
    def post(self, request: Request) -> Response:
        email: str = request.data[EMAIL]
        nickname: str = request.data[NICKNAME]
        password: str = request.data[PASSWORD]
        name: str = request.data[NAME]
        phone_number: str = request.data[PHONE_NUMBER]
        verification_code: str = request.data[VERIFICATION_CODE]

        if not self.is_valid_email(email):
            return self.get_error_response("유효하지 않은 형식의 이메일입니다.")

        if not is_verification_valid(phone_number, verification_code):
            return self.get_error_response("유효하지 않은 인증 정보입니다.")

        remove_verification(phone_number)

        if User.objects.filter(email=email).exists() or Profile.objects.filter(phone_number=phone_number).exists():
            return self.get_error_response("이미 존재하는 회원입니다.")

        user: User = User.objects.create_user(username=str(uuid1()), password=password, email=email)
        profile: Profile = Profile(user=user, nickname=nickname, name=name, phone_number=phone_number)
        user.save()
        profile.save()

        token: Token = Token.objects.create(user=user)
        return Response({TOKEN: token.key})

    @staticmethod
    def is_valid_email(email: str):
        try:
            EmailField().clean(email)
            return True
        except ValidationError:
            return False
