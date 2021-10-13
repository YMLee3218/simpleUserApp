from rest_framework.views import APIView
from rest_framework.response import Response

MESSAGE = "message"


class MyAPIView(APIView):
    @staticmethod
    def get_error_response(message: str, status=400) -> Response:
        return MyAPIView.get_message_response(message, status)

    @staticmethod
    def get_message_response(message: str, status=200) -> Response:
        return Response({MESSAGE: message}, status=status)
