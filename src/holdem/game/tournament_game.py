from threading import Thread
from time import sleep
from holdem.game.game import Game
from core.blinds.scheme.scheme import Scheme
from holdem.network import Network
from special.debug import Debug


class TournamentGame(Game):

    def __init__(self, id_: int, name: str, total: int, bots: int, stack: int, seats: int, blinds: Scheme,
                 start_blinds: int, password: str):

        super().__init__(id_, total, seats, stack, blinds)

        self.network = Network({'type': 'gh',
                                'id': self.id,
                                'game type': 'tournament',
                                'name': name,
                                'total players': total,
                                'initial stack': stack,
                                'table seats': seats,
                                'password': password,
                                'players left': bots})

        self.network.send({'type': 'start registration'})

        if total == bots:
            self.network.send({'type': 'start game'})

        self.online = True

        for _ in range(bots):
            self.add_bot_player()

        if start_blinds == 1:
            self.blinds.curr_round = -1

        elif start_blinds == 2:
            self.blinds.curr_round = 3

        elif start_blinds == 3:
            self.blinds.curr_round = 11

        Thread(target=lambda: self.network_process()).start()

        if total == bots:
            Thread(target=lambda: self.wait_for_end(), name=f'Game {self.id}: wait for end').start()
            Thread(target=lambda: self.send_players_left(), 
                   name=f'Game {self.id}: send players left').start()

    def network_process(self):

        Debug.game_manager(f'Game {self.id}: ready to listen game')

        while True:

            try:

                request = self.network.receive()

                Debug.game_manager(f'Game {self.id}: message {request}')

                if request['type'] == 'add player' and not self.game_started:
                    Debug.game_manager(f'Game {self.id}: add player')
                    if self.add_real_player(request['name']):
                        self.network.send({'type': 'start game'})
                        Thread(target=lambda: self.wait_for_end(), name=f'Game {self.id}: wait for end').start()
                        Thread(target=lambda: self.send_players_left(), 
                               name=f'Game {self.id}: send players left').start()

                    else:
                        self.network.send({'type': 'update players', 'left': self.players_count})

                elif request['type'] == 'delete player' and not self.game_started:
                    Debug.game_manager(f'Game {self.id}: delete player')
                    self.delete_player(request['name'])

                elif request['type'] == 'break':
                    Debug.game_manager(f'Game {self.id}: break game')
                    self.break_game()

                    if self.thread:
                        self.thread.join()

                    self.network.send({'type': 'broken'})

            except ValueError:
                continue

            except IndexError:
                continue

    def wait_for_end(self) -> None:

        self.thread.join()

        if not self.game_broken:
            self.network.send({'type': 'end game'})

    def send_players_left(self) -> None:
        
        while self.thread.is_alive():
            if self.players_left is not None:
                self.network.send({'type': 'update players', 'left': self.players_left})
                sleep(5)
