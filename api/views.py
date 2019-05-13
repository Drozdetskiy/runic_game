from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def my_first_api_view(request, *args, **kwargs):
    return Response(data={
        'status': f'{request.user}'
}, status=202)
