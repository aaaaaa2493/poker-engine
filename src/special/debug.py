class Debug:
    Debug = 0
    Table = 0
    Decision = 0
    InputDecision = 0
    Resitting = 0
    Standings = 0
    GameProgress = 0
    Evolution = 1
    PlayManager = 1
    GameManager = 1
    Parser = 1
    Learning = 1
    DataSets = 0
    UnitTest = 1
    Error = 1

    if Table:
        @staticmethod
        def table(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def table(*args, **kwargs):
            pass

    if Decision:
        @staticmethod
        def decision(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def decision(*args, **kwargs):
            pass

    if InputDecision:
        @staticmethod
        def input_decision(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def input_decision(*args, **kwargs):
            pass

    if Resitting:
        @staticmethod
        def resitting(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def resitting(*args, **kwargs):
            pass

    if Standings:
        @staticmethod
        def standings(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def standings(*args, **kwargs):
            pass

    if GameProgress:
        @staticmethod
        def game_progress(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def game_progress(*args, **kwargs):
            pass

    if GameManager:
        @staticmethod
        def game_manager(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def game_manager(*args, **kwargs):
            pass

    if Evolution:
        @staticmethod
        def evolution(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def evolution(*args, **kwargs):
            pass

    if PlayManager:
        @staticmethod
        def play_manager(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def play_manager(*args, **kwargs):
            pass

    if Parser:
        @staticmethod
        def parser(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def parser(*args, **kwargs):
            pass

    if Learning:
        @staticmethod
        def learning(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def learning(*args, **kwargs):
            pass

    if DataSets:
        @staticmethod
        def datasets(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def datasets(*args, **kwargs):
            pass

    if UnitTest:
        @staticmethod
        def unit_test(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def unit_test(*args, **kwargs):
            pass

    if Error:
        @staticmethod
        def error(*args, **kwargs):
            print(*args, **kwargs)
    else:
        @staticmethod
        def error(*args, **kwargs):
            pass
