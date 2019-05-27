import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from api.models import Game
from api.serializers import UserSerializer, GameSerializer
from rest_framework import permissions

from api.game.web_game import GameQueue


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


class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameMaster(APIView):
    def data_base_save(self, game):
        if game.turn == 10:
            user = User.objects.get(id=game.player_id)
            player_number = game.player_number
            if getattr(game, f'player_{player_number}').score == 5:
                game_status = 'draw'
            elif getattr(game, f'player_{player_number}').score < 5:
                game_status = 'loose'
            else:
                game_status = 'win'

            user_game = Game(
                game_history=game.game_history,
                owner=user,
                score=getattr(game, f'player_{player_number}').score,
                status=game_status
            )
            user_game.save()

    def get(self, request, game_hash):
        game = GameQueue.game_queue.get(game_hash, None)
        if game:
            game.next_turn_bot()
            self.data_base_save(game)
            return Response(game.json_repr)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, game_hash):
        game = GameQueue.game_queue.get(game_hash, None)
        if game:
            print(request.data)
            user_data = request.data
            card_index = user_data['player_turn']['card_index']
            i = user_data['player_turn']['i']
            j = user_data['player_turn']['j']
            game.next_turn(card_index, i, j)
            self.data_base_save(game)
            return Response(game.json_repr)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GameUrl(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        token = Token.objects.get(key=user_token)
        user_id = token.user_id

        return Response(
            json.dumps(
                {'game_hash': GameQueue.get_new_game(user_id)}
            )
        )


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserSerializer
