import json
import os
import hashlib
import sys
import time

from colorama import Fore

class ChessDatabase:
    def __init__(self):
        pass

    def load_pgn(self, input_pgn_file_name, verbose = False) -> bool:
        try:
            if verbose:
                print(f"Load file: {input_pgn_file_name}... ", end="")


            file = open(input_pgn_file_name, "r")
            self.pgn_file = file.read()
            file.close()

        except Exception as e:
            if verbose:
                print("ERROR")
            return False

        if verbose:
            print("OK")

        return True

    def __get_games(self):

        games = []
        game = ''
        append = False

        for row in self.pgn_file.split("\n"):
            if '[' in row:  # salto se la riga contiente [, ossia informazioni sulla partita
                continue

            if row == '':
                if append:
                    append = False
                    games.append(game)
                    game = ''
                continue

            if not append and row[0] == '1':
                append = True

            if append:
                game += str(row)

        if game != '':
            games.append(game)

        return games

    def store_games(self, database_file_name="database.json", check_file_name="check.json", verbose=False):
        #try:

            db_file_content = '''
                            {
                                "n": 0,
                                "sha": [],
                                "tree": {}
                            }
                            '''

            if os.path.exists(database_file_name):
                db_file = open(database_file_name, "r")
                _db_file_content = db_file.read()
                if _db_file_content.strip() != "":
                    db_file_content = _db_file_content
                db_file.close()

            db_file_content = json.loads(db_file_content)

            games = self.__get_games()

            index = 0
            l = len(games)
            for game in games:
                print(Fore.RESET, end="")

                sha_game = hashlib.sha256(game.replace(" ", "").encode()).hexdigest()

                if sha_game in db_file_content["sha"]:
                    if verbose:
                        print(Fore.RED + f"{sha_game} is already in the database")
                    continue

                db_file_content["sha"].append(sha_game)
                db_file_content["n"] += 1
                self.add_to_tree(self.__get_game_handle(game), db_file_content["tree"], verbose=verbose)

                if verbose:
                    index += 1
                    if index == l:
                        print(Fore.GREEN + f"\n{index}/{l} - {100 * index / l}%")
                    else:
                        print(Fore.YELLOW + f"\n{index}/{l} - {100 * index / l}%")


            # salvo le modifiche
            db_file = open(database_file_name, "w")
            db_file.write(json.dumps(db_file_content))
            db_file.close()

        #except Exception as e:
        #    print("ERROR: ", e)

    def __get_game_handle(self, game):
        try:
            moves_raw = game.split(" ")

            result = 'f'
            if moves_raw[-1] == "1-0":
                result = 'w'
            elif moves_raw[-1] == "0-1":
                result = 'b'

            # elimino il risultato finale
            del moves_raw[-1]

            moves = []
            # elimino il numero della mossa e ''
            for move in moves_raw:
                if move != '':
                    if '.' in move:
                       moves.append(move[move.index('.')+1::])
                    else:
                        moves.append(move)


            return {
                "result_raw": moves_raw[-1],
                "result": result,
                'moves': moves
            }

        except Exception as e:
            print("ERROR: ", e)


    '''

        "tree": {
            "e4": {
                "move": "e4",
                "n": 100,
                "w": 50,
                "b": 30,
                "f": 20,
                "next": {
                    "e5": {...},
                    "d5": {...}
                }
            },              
            ...
        }
    '''
    def add_to_tree(self, game, tree={}, lv=0, verbose=False):

        if len(game["moves"]) == lv:
            return
        else:

            if verbose:
                print(f'{lv + 1}/{len(game["moves"])} (move: {game["moves"][lv]})')

            # controllo se c'è una mossa nell'albero delle mosse che sia uguale a quella giocata
            if game["moves"][lv] in tree:       # mossa esistente

                # aggiorno i valori di vittoria e partite giocate della mossa nell'albero
                tree[game["moves"][lv]]["n"] += 1
                tree[game["moves"][lv]][game["result"]] += 1

            else:       # non trovando già la mossa nel database, la aggiungo

                tree[game["moves"][lv]] = {         # aggiungo la nuova mossa
                    "move": game["moves"][lv],
                    "n": 0,
                    "w": 0,
                    "b": 0,
                    "f": 0,
                    "next": {}
                }

                # aggiorno i valori di vittoria e partite giocate della mossa nell'albero
                tree[game["moves"][lv]]["n"] += 1
                tree[game["moves"][lv]][game["result"]] += 1

            self.add_to_tree(game, tree[game["moves"][lv]]["next"], lv + 1, verbose)


if __name__ == '__main__':

    print(Fore.RESET, end="")

    # x.py input_file_name.pgn [flags]
    # flags:
    # -v -> verbose

    verbose = False
    if '-v' in sys.argv:
        start = time.time()
        verbose = True
        print("Input file: ", sys.argv[1])
        print("Mode: verbose\n")

    cd = ChessDatabase()
    cd.load_pgn(sys.argv[1], verbose)
    cd.store_games(verbose=verbose)

    if verbose:
        end = time.time()
        print(Fore.MAGENTA + "\n\nExecution time: ", str(end - start))

    print(Fore.RESET, end="")

'''
{"n": 318, "sha": [], "tree": {
    "e4": {
        "move": "e4",
        "n": 100,
        "w": 50,
        "b": 30,
        "f": 20,
        "next": {
            "e5": {
            "move": "e5",
            "n": 100,
            "w": 50,
            "b": 30,
            "f": 20,
            "next": {
            "e3": {
                "move": "e3",
                "n": 200,
                "w": 150,
                "b": 30,
                "f": 20,
                "next": { }
            }}
        },
        "d5": {
            "move": "d5",
            "n": 200,
            "w": 150,
            "b": 30,
            "f": 20,
            "next": { }
        }}
    },
    "d4": {
        "move": "d4",
        "n": 200,
        "w": 150,
        "b": 30,
        "f": 20,
        "next": { }
    }

}}'''