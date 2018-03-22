from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comun.utils import ProcessExcel


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        try:
            file = request.FILES['file']
            ProcessExcel(instance=file)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response('successfully saved', status=status.HTTP_201_CREATED)
