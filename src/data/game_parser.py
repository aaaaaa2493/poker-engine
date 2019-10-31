from typing import Optional, List
from os import listdir, makedirs
from os.path import exists
from shutil import copyfile
from data.game_model.poker_game import PokerGame
from data.game_model.game_source import GameSource
from data.reg_ex.poker_stars import PokerStars
from data.reg_ex.party_poker import PartyPoker
from data.reg_ex.poker_888 import Poker888
from data.parsing.poker_stars_parsing import PokerStarsParsing
from data.parsing.party_poker_parsing import PartyPokerParsing
from data.parsing.poker_888_parsing import Poker888Parsing
from special.debug import Debug


class GameParser:

    @staticmethod
    def get_parser(text, game):
        match = PokerStars.identifier.search(text)
        if match is not None:
            Debug.parser('Found PokerStars game')
            game.game_source = GameSource.PokerStars
            return PokerStarsParsing(game)

        match = Poker888.identifier.search(text)
        if match is not None:
            Debug.parser('Found Poker888 game')
            game.game_source = GameSource.Poker888
            return Poker888Parsing(game)

        match = Poker888.identifier_snap.search(text)
        if match is not None:
            Debug.parser('Found Poker888 Snap Poker game')
            game.game_source = GameSource.Poker888
            return Poker888Parsing(game, True)

        match = PartyPoker.identifier.search(text)
        if match is not None:
            Debug.parser('Found PartyPoker game')
            game.game_source = GameSource.PartyPoker
            return PartyPokerParsing(game)

        return None

    @staticmethod
    def parse_dir(path: str, need_convert: bool, need_output: bool) -> List[PokerGame]:
        parsed = []
        games = listdir(PokerGame.path_to_raw_games + path)
        if not exists(PokerGame.path_to_parsed_games + path):
            makedirs(PokerGame.path_to_parsed_games + path)
        for game_path in games:
            game = GameParser.parse_game(f'{path}/{game_path}')
            if game is not None:
                if need_output:
                    parsed += [game]
                game.save()
                if need_convert:
                    game.convert()
                # remove(PokerGame.path_to_raw_games + path + '/' + game_path)
        return parsed

    @staticmethod
    def search_in_dir(path: str, line: str) -> None:
        games = listdir(PokerGame.path_to_raw_games + path)
        for game_path in games:
            game_path = f'{path}/{game_path}'
            text_game = open(PokerGame.path_to_raw_games + game_path, 'r', encoding='utf-8').read().strip()
            if line in text_game:
                Debug.parser('FOUND', line, ':', game_path)

    @staticmethod
    def copy_dir(src: str, dst: str) -> None:
        if exists(PokerGame.path_to_raw_games + src) and exists(PokerGame.path_to_raw_games + dst):
            for name in listdir(PokerGame.path_to_raw_games + src):
                copyfile(PokerGame.path_to_raw_games + src + '/' + name,
                         PokerGame.path_to_raw_games + dst + '/' + name)

    @staticmethod
    def parse_game(path: str) -> Optional[PokerGame]:
        game = PokerGame()
        text_game = open(PokerGame.path_to_raw_games + path, 'r', encoding='utf-8').read().strip()
        game.source = path

        Debug.parser('\nStarting to analyse ' + path)

        parser = GameParser.get_parser(text_game, game)

        if parser is None:
            Debug.parser('Cannot parse game - can not identify')
            return None

        parser.process_game(text_game)

        game.approximate_players_left()
        game.add_final_table_marks()
        return game
