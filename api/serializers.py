from django.contrib.auth.models import User
from  rest_framework import serializers

from api.models import Game


class UserSerializer(serializers.HyperlinkedModelSerializer):
    api_game = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Game.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_history', 'score', 'status')
