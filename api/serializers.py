from django.contrib.auth import get_user_model
from  rest_framework import serializers

from api.models import Game


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password")


class GameSerializer(serializers.ModelSerializer):
    # api_game = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = UserSerializer()

    class Meta:
        model = Game
        fields = ('id', 'game_history', 'owner', 'score', 'status')
