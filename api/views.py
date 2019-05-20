import json

from django.contrib.auth.models import User

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from api.models import Game
from api.serializers import UserSerializer, GameSerializer
from rest_framework import permissions


@api_view(['GET'])
def my_first_api_view(request, *args, **kwargs):
    return Response(data={
        'status': f'{request.auth}'
}, status=202)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class Tmp(APIView):
    def get(self, request, format=None):
        return Response(json.dumps({"table": [{"top": 7, "bot": 7, "left": 4, "right": 2, "player": 1}, {"top": 1, "bot": 7, "left": 7, "right": 8, "player": 1}, {"top": 0, "bot": 0, "left": 0, "right": 0, "player": 0}, {"top": 3, "bot": 5, "left": 5, "right": 5, "player": 2}, {"top": 3, "bot": 5, "left": 7, "right": 6, "player": 1}, {"top": 9, "bot": 7, "left": 3, "right": 6, "player": 1}, {"top": 0, "bot": 0, "left": 0, "right": 0, "player": 0}, {"top": 0, "bot": 0, "left": 0, "right": 0, "player": 0}, {"top": 0, "bot": 0, "left": 0, "right": 0, "player": 0}], "player_1_hand": [{"top": 3, "bot": 5, "left": 5, "right": 5, "player": 1}, {"top": 3, "bot": 1, "left": 7, "right": 2, "player": 1}], "player_2_hand": [{"top": 9, "bot": 7, "left": 3, "right": 6, "player": 2}, {"top": 8, "bot": 4, "left": 4, "right": 8, "player": 2}, {"top": 3, "bot": 1, "left": 7, "right": 2, "player": 2}], "turn": 6, "player_1_score": 6, "player_2_score": 4, "card_queue_1": [0, 1], "card_queue_2": [0, 1, 2], "name_player_1": "admin", "name_player_2": "admin"}))