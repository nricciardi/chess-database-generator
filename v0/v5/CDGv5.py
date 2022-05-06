import json
import os
import hashlib
from colorama import Fore

class ChessDatabaseGenerator:
    def __init__(self):
        self.database_file_content = None
        self.check_file_content = None
        print(Fore.RESET, end="")

    def __del__(self):
        print(Fore.RESET, end="")

    def __load_pgn(self, input_pgn_file_name, mark=False, verbose=False):

        pgn_file = None

        try:
            if verbose:
                print(Fore.RESET + f"\nLoad games from PGN file: {input_pgn_file_name}... ", end="")


            file = open(input_pgn_file_name, "r")
            pgn_file = file.read()
            file.close()

            if verbose:
                print(Fore.GREEN + "OK" + Fore.RESET)

            # se richiesto aggiungo il mark al file
            if mark:

                if verbose:
                    print(Fore.RESET + f"Mark PGN file: {input_pgn_file_name}... ", end="")

                os.rename(input_pgn_file_name, input_pgn_file_name + ".done")

                if verbose:
                    print(Fore.GREEN + "OK" + Fore.RESET)

        except Exception as e:
            if verbose:
                print(Fore.RED + "ERROR" + Fore.RESET)
            return None

        return pgn_file

    def load_database(self, database_file_name, verbose = False) -> bool:
        try:
            if verbose:
                print(Fore.RESET + f"\nLoad database: {database_file_name}... ", end="")

            self.database_file_content = self.__read_database_file(database_file_name)

        except Exception as e:
            if verbose:
                print(Fore.RED + "ERROR" + Fore.RESET)
            return False

        if verbose:
            print(Fore.GREEN + "OK" + Fore.RESET)

        return True

    def load_check_file(self, check_file_name, verbose = False) -> bool:
        try:
            if verbose:
                print(Fore.RESET + f"\nLoad check file: {check_file_name}... ", end="")


            self.check_file_content = self.__read_check_file(check_file_name)

        except Exception as e:
            if verbose:
                print(Fore.RED + "ERROR" + Fore.RESET)
            return False

        if verbose:
            print(Fore.GREEN + "OK" + Fore.RESET)
    
    def __read_database_file(self, database_file_name):
        database_file_content = '''
                                    { }
                                    '''
        try:
            if os.path.exists(database_file_name):
                return json.load(database_file_name)

        except Exception as e:
            return database_file_content

        return database_file_content


    def __write_file(self, file_name, content, verbose=False, json_content=True):

        if verbose:
            print(Fore.RESET + f"Write file: {file_name}... ", end="")

        if json_content:
            json.dump(content, file_name)
        else:
            # salvo le modifiche
            db_file = open(file_name, "w")
            db_file.write(content)
            db_file.close()

        if verbose:
            print(Fore.MAGENTA + "END" + Fore.RESET)

    def __read_check_file(self, check_file_name):

        check_file_content = '''
                                {
                                    "n": 0,
                                    "sha": []
                                }
                                '''
        try:
            if os.path.exists(check_file_name):
                return json.load(check_file_name)

        except Exception as e:
            return check_file_content

        return check_file_content

    def backup(self, database_file_name="database.json", check_file_name="check.json", verbose=False):
        try:

            database_backup_file_name = database_file_name[
                                        :database_file_name.index('.')] + ".backup." + database_file_name[
                                                                                       database_file_name.index(
                                                                                           '.') + 1:]

            if verbose:
                print(f"Backup: {database_backup_file_name}... ", end="")

            # salvo le modifiche
            self.__write_file(database_backup_file_name, json.dumps(self.database_file_content), False)
            if verbose:
                print(Fore.GREEN + "OK" + Fore.RESET)

            check_backup_file_name = check_file_name[:check_file_name.index('.')] + ".backup." + check_file_name[
                                                                                                 check_file_name.index(
                                                                                                     '.') + 1:]

            if verbose:
                print(f"Backup: {check_backup_file_name}... ", end="")

            self.__write_file(check_backup_file_name, json.dumps(self.check_file_content), False)

            if verbose:
                print(Fore.GREEN + "OK" + Fore.RESET)

        except Exception as e:
            if verbose:
                print(Fore.RED + "ERROR: " + str(e) + Fore.RESET)

    def store(self, database_file_name="database.json", check_file_name="check.json", verbose=False, backup=True):

        try:
            # se richiesto faccio il backup del file prima di manipolarli
            if backup:
                self.backup(database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose)

            if verbose:
                print(Fore.RESET + f"Store database in {database_file_name}... ", end="")

            self.__write_file(database_file_name, json.dumps(self.database_file_content), False)

            if verbose:
                print(Fore.GREEN + "OK" + Fore.RESET)

            if verbose:
                print(Fore.RESET + f"Store check sha in {check_file_name}... ", end="")

            self.__write_file(check_file_name, json.dumps(self.check_file_content), False)

            if verbose:
                print(Fore.GREEN + "OK" + Fore.RESET)

        except Exception as e:
            if verbose:
                print(Fore.RED + "ERROR: " + str(e) + Fore.RESET)

    def __get_games(self, pgn_file):

        games = []
        game = ''
        append = False

        for row in pgn_file.split("\n"):
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

    def store_games(self, pgn_file_name, mark=False, database_file_name="database.json", check_file_name="check.json", verbose=0, backup=False, load=True, store=True):
        #try:

            # recupera il file pgn
            pgn_file = self.__load_pgn(input_pgn_file_name=pgn_file_name, mark=mark, verbose=verbose)

            if pgn_file == None:
                if verbose:
                    print(Fore.RED + "Error while opening the file" + Fore.RESET)

                return None

            if load:
                self.load_database(database_file_name)
                self.load_check_file(check_file_name)


            # se richiesto faccio il backup del file prima di manipolarli
            if store and backup:
                self.backup(database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose)


            games = self.__get_games(pgn_file)

            index = 0
            added = 0
            l = len(games)
            for game in games:

                index += 1

                sha_game = hashlib.sha256(game.replace(" ", "").encode()).hexdigest()

                if sha_game in self.check_file_content["sha"]:
                    if verbose:
                        print(Fore.RED + f"{sha_game} is already in the database"  + Fore.RESET, end="")
                        print(f" ({index}/{l} - {round(100 * (index) / l, 2)}%)" + Fore.RESET)
                    continue

                self.check_file_content["sha"].append(sha_game)
                self.check_file_content["n"] += 1
                self.add_to_tree(self.__get_game_handle(game), self.database_file_content, verbose=verbose)
                added += 1

                if verbose:
                    if index == l:
                        print(Fore.GREEN + f"Add to tree... {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET)
                    else:
                        print(Fore.YELLOW + f"Add to tree... {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET, end="\r\r")

            # salvo le modifiche
            if store:
                self.store(database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose)


            return added

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

            if verbose == 2:
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