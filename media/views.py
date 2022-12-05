from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from media.utils import print_message


class TestSendTask(APIView):
    def get(self, request):
        print_message.delay('hello world')
        return Response(data={'hello': 'bello'}, status=status.HTTP_200_OK)
