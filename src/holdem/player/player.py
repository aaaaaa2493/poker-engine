from datetime import datetime
from typing import Tuple
from holdem.play.result import Result
from holdem.play.option import Option
from holdem.poker.hand import Hand
from core.cards.cards_pair import CardsPair
from holdem.play.play import Play
from holdem.base_network import BaseNetwork
from core.cards.card import Card


class Player:

    def __init__(self, _id: int, money: int, controlled: bool, name: str, play: Play, net: BaseNetwork):

        self.id: int = _id
        self.name: str = name
        self.money: int = money
        self.money_start_of_hand: int = money
        self.gived: int = 0
        self.in_pot: int = 0
        self.wins: int = 0
        self.in_game: bool = False
        self.in_play: bool = True
        self.re_seat: Players = None
        self.cards: CardsPair = CardsPair()
        self.hand: Hand = None
        self.controlled: bool = controlled
        self.lose_time: int = None
        self.play: Play = play
        self.network: BaseNetwork = net

    def __str__(self):

        return f'player {self.name} with {self.money} stack and {self.get_cards()}'

    def get_cards(self) -> str:

        return str(self.cards)

    def pay(self, money: int) -> int:

        money = min(money, self.remaining_money())

        self.money -= money - self.gived
        self.gived = money

        return money

    def move_money_to_pot(self) -> int:

        self.in_pot += self.gived
        paid = self.gived
        self.gived = 0
        return paid

    def drop_cards(self) -> None:

        self.cards.drop()

    def fold(self) -> None:

        self.drop_cards()
        self.in_game = False

    def remaining_money(self) -> int:

        return self.money + self.gived

    def go_all_in(self) -> int:

        return self.pay(self.remaining_money())

    def in_all_in(self) -> bool:

        return self.in_game and self.money == 0

    def in_game_not_in_all_in(self) -> bool:

        return self.in_game and self.money > 0

    def add_card(self, card: Card) -> None:

        self.cards.set(card)

    def was_resit(self) -> None:

        self.re_seat = None

    def can_resit(self) -> bool:

        return self.re_seat is None

    def wait_to_resit(self) -> bool:

        return self.re_seat is not None

    def set_lose_time(self, stack: int = 0, place: int = 0) -> None:

        self.lose_time = int(datetime.now().timestamp() * 10 ** 6) * 10 ** 2 + stack * 10 + place

    def make_decision(self, **kwargs) -> Result:
        if not self.in_game:
            return Result.DoNotPlay

        if self.money == 0 and self.in_game:
            return Result.InAllin

        answer, raised_money = self._decide(**kwargs)
        raised_money = int(raised_money)

        if answer is Option.Fold:
            self.fold()
            return Result.Fold

        elif answer is Option.CheckCall:
            to_call: int = kwargs['to_call']
            if self.remaining_money() > to_call:
                #  Если игрок вернул CheckCall но колоть нечего то очевидно чек
                if to_call == 0 or self.gived == to_call:
                    return Result.Check
                else:
                    self.pay(to_call)
                    return Result.Call
            else:
                self.go_all_in()
                return Result.Call

        elif answer is Option.Raise:
            to_call = kwargs['to_call']
            min_raise = kwargs['min_raise']
            if self.remaining_money() > to_call:

                if raised_money < min_raise:
                    raised_money = min_raise

                if raised_money > self.remaining_money():
                    raised_money = self.remaining_money()

                if raised_money == self.remaining_money():
                    self.go_all_in()
                    return Result.Allin

                self.pay(raised_money)
                return Result.Raise

            else:
                self.go_all_in()
                return Result.Call

        else:
            self.fold()
            return Result.Fold

    def _decide(self, **kwargs) -> Tuple[Option, int]:
        raise NotImplementedError('decide')
