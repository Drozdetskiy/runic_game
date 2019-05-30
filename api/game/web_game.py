import secrets
import time
from random import randint

from api.ai_v_0_3.ai import AIPlayer
from api.game.game import Game


class GameQueue:
    game_queue = {}

    @classmethod
    def _queue_clearing(cls):
        now = time.time()
        for game_hash, game in cls.game_queue:
            if now - game.created_at > ServerSettings.CRITICAL_QUEUE_TIME:
                del cls.game_queue[game_hash]

    @classmethod
    def get_new_game(cls, name):
        game_hash = secrets.token_urlsafe()
        cls.game_queue[game_hash] = WebGame(name)
        if len(cls.game_queue) > ServerSettings.CRITICAL_QUEUE_LENGTH:
            cls._queue_clearing()
        return game_hash


class ServerSettings:
    CRITICAL_QUEUE_LENGTH = 30
    CRITICAL_QUEUE_TIME = 3600


class WebGame(Game):
    def __init__(self, user_id):
        player_number = randint(1, 2)
        bot_number = 2 if player_number == 1 else 1
        self.player_number = player_number
        self.bot_number = bot_number
        self.created_at = time.time()
        self.game_history = {}
        self.player_id = user_id
        super().__init__()

    def next_turn(self, card_index, i, j, get_player=0):
        player_turn = 1 if self.turn % 2 else 2
        if self.player_number == player_turn:
            super().next_turn(card_index, i, j, get_player=player_turn)

    def next_turn_bot(self):
        player_turn = 1 if self.turn % 2 else 2
        if self.bot_number == player_turn:
            bot_player = AIPlayer(self, self.bot_number)
            super().next_turn(*bot_player.make_choise())

    def _do_json(self):
        _res = super().json_repr
        _res["card_queue_1"] = list(range(len(_res["player_1_hand"])))
        _res["card_queue_2"] = list(range(len(_res["player_2_hand"])))
        _res["player_number"] = self.player_number
        _res["bot_number"] = self.bot_number
        return _res

    @property
    def json_repr(self):
        return self.game_history.setdefault(self.turn, self._do_json())
