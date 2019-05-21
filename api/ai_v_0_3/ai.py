from copy import deepcopy
from functools import reduce
from random import randint, shuffle

from api.game.game import Game, CardLogic, input_card


class AISettings:
    def_priority = 1
    lose_def_priority = 0


class RandomSituation(Game):
    def __init__(self, **kwargs):
        mods = kwargs
        super().__init__(**mods)
        self.cell_queue = [
            (i, j)
            for i in range(self.table.side)
            for j in range(self.table.side)
        ]
        self.rand_turn_number = randint(1, 9)

    def make_rand_situation(self):
        shuffle(self.player_1.hand)
        shuffle(self.player_2.hand)
        shuffle(self.cell_queue)

        for turn_number in range(1, self.rand_turn_number):
            self.next_turn(
                0,
                *self.cell_queue.pop()
            )


class AIPlayer:
    def __init__(self, game, player_number=1):
        self.game = deepcopy(game)
        self.player_number = player_number
        self.enemy_number = 2 if player_number == 1 else 1

    def _add_enemy_influence(
            self,
            card,
            add_neutral_influence=False
    ):
        if card.influence or add_neutral_influence:
            if not card.weakness:
                game_model = deepcopy(self.game)
                game_model.next_turn(
                    card.card_number,
                    *card.coords,
                    get_player=self.player_number
                )
                enemy_hand = AIPlayerHand(game_model, self.enemy_number)
                card.weakness -= max(enemy_hand.card_rating).attack_position \
                    if enemy_hand.card_rating else 0

    def make_choise(self):
        player_hand = AIPlayerHand(self.game, self.player_number)
        player_choise = player_hand.card_rating
        for card in player_choise:
            self._add_enemy_influence(card)

        chosen_card = max(player_choise)
        if not chosen_card.influence:
            for card in player_choise:
                self._add_enemy_influence(card, add_neutral_influence=True)
        return (chosen_card.card_number, *chosen_card.coords)


class AIPlayerHand:
    def __init__(self, game, player_number=1):
        self.game = deepcopy(game)
        self.player_number = player_number
        self.enemy_number = 2 if player_number == 1 else 1
        self.cell_queue = [
            (i, j) for i in range(game.table.side)
            for j in range(game.table.side)
        ]
        self._rated_cards_list = []

    def compare_sides(self, card):
        enemy_player = getattr(
                    self.game, f'player_{self.enemy_number}'
                )
        return {
            comparing: reduce(
                lambda s, enemy_card:
                s + (1 if getattr(card, comparing[0]) <
                        getattr(enemy_card, comparing[1]) else 0),
                enemy_player.hand,
                0
            ) for comparing in CardLogic.COMPARE_QUEUE
        }

    def get_priority_sides(self, i, j):
        priority = []
        neighboors = self.game.table.neighbours[(i, j)]
        for order_number, neighboor in enumerate(neighboors):
            x, y = neighboor or (None, None)
            neighboor_player = self.game.table.table[x][y].player \
                if neighboor else 1
            if not neighboor_player:
                priority.append(
                    CardLogic.COMPARE_QUEUE[order_number]
                )
        return priority

    def card_positions(self, card):
        def_positions = {}
        attack_positions = {}
        comparing_card_sides = self.compare_sides(card)

        for i, j in self.cell_queue:
            if not self.game.table.table[i][j].player:
                comparing_card_list = []
                for priority in self.get_priority_sides(i, j):
                    comparing_card_list.append(
                        comparing_card_sides[priority]
                    )
                def_positions[(i, j)] = AISettings.def_priority \
                    if not sum(comparing_card_list) \
                    else AISettings.lose_def_priority

                local_game = deepcopy(self.game)
                attack_positions[(i, j)] = local_game.table.place_card(
                    i, j, card
                )
        return def_positions, attack_positions

    def make_rated_cards_list(self):
        player_hand = getattr(
            self.game,
            f'player_{self.player_number}'
        ).hand
        for card_number, card in enumerate(player_hand):
            def_dict, attack_dict = self.card_positions(card)
            for key, value in def_dict.items():
                self._rated_cards_list.append(
                    RatedCard(
                        card=card,
                        card_number=card_number,
                        def_position=value,
                        attack_position=attack_dict[key],
                        coords=key,
                    )
                )

    @property
    def card_rating(self):
        if not self._rated_cards_list:
            self.make_rated_cards_list()
        return self._rated_cards_list


class RatedCard(CardLogic):
    def __init__(
            self,
            card,
            card_number,
            def_position,
            attack_position,
            coords
    ):
        self.card = card
        self.card_number = card_number
        self.def_position = def_position
        self.attack_position = attack_position
        self.weakness = 0
        self.coords = coords
        self.power = reduce(
            lambda s, x: s + x,
            (getattr(card, side) for side in self.CARD_SIDE_QUEUE)
        )

    @property
    def influence(self):
        return self.def_position + self.attack_position + self.weakness

    def __gt__(self, other):
        card_position = self.def_position + self.attack_position +\
                        self.weakness
        other_position = other.def_position + other.attack_position + \
                        other.weakness

        if card_position != other_position:
            return card_position > other_position
        return self.power < other.power

    def __repr__(self):
        return '-'.join(
            map(
                str,
                (
                    self.card.__repr__(),
                    self.coords,
                    self.def_position + self.attack_position + self.weakness
                )
            )
        )


def rand_game_emul():
    rand_game = RandomSituation()
    rand_game.make_rand_situation()
    rand_game.res()

    ai = AIPlayer(rand_game, 1)
    print(ai.make_choise())


def main():
    g = Game()
    print('Start Game')
    for turn in range(9):
        g.res()
        if not turn % 2:
            print(f'player {turn % 2} turn')
            card_index, i, j = input_card()
            g.next_turn(card_index, i, j)
        else:
            ai_player = AIPlayer(g, 2)
            g.next_turn(*ai_player.make_choise())
    g.res()


if __name__ == '__main__':
    main()
