from CDGv5 import ChessDatabaseGenerator as cdg
import time
import multiprocessing
from colorama import Fore, init
init()
import glob
import sys

def help():

    title = '''  ______ _                        _____                  _                          ______                                              
 / _____) |                      (____ \       _        | |                        / _____)                             _               
| /     | | _   ____  ___  ___    _   \ \ ____| |_  ____| | _   ____  ___  ____   | /  ___  ____ ____   ____  ____ ____| |_  ___   ____ 
| |     | || \ / _  )/___)/___)  | |   | / _  |  _)/ _  | || \ / _  |/___)/ _  )  | | (___)/ _  )  _ \ / _  )/ ___) _  |  _)/ _ \ / ___)
| \_____| | | ( (/ /|___ |___ |  | |__/ ( ( | | |_( ( | | |_) | ( | |___ ( (/ /   | \____/( (/ /| | | ( (/ /| |  ( ( | | |_| |_| | |    
 \______)_| |_|\____|___/(___/   |_____/ \_||_|\___)_||_|____/ \_||_(___/ \____)   \_____/ \____)_| |_|\____)_|   \_||_|\___)___/|_|    
                                                                                                                                        '''

    print(Fore.BLUE + title + Fore.RESET, end= "\n\t\tby Nicola Ricciardi\n\n" + Fore.RESET)
    message = '''CDG-cli.py [-flag] <value>
    
    flags:
    -v <level> -> verbose level (0, 1, 2); default 0
    -a <path> -> loads all file .pgn in root
    -c <check_file_name> -> use an existed sha control file
    -d <database_file_name> -> use an existed database file
    -i <input_file_name> -> loads only the input file
    -h -> get help
    -b -> backup database and check file each store
    -m -> mark file loaded
    
    # Only for -a:
    -l <value > 0> -> load database and check file each <value> add; 0: never, 1: each add, ... 
    -s <value > 0> -> store database and check file each <value> add; 0: never, 1: each add, ...
    -p <core> -> enable multiprocessing on n core; -1 = cpu_core()
    
    Database Chess Generator version 0.5.2
'''

    print(message)
    print()

if __name__ == '__main__':

    print(Fore.RESET, end="")

    # default
    verbose = 0
    backup = False
    input_file_name = "input.pgn"
    check_file_name = "check.json"
    load_value = 0
    store_value = 0
    mark = False
    database_file_name = "database.json"

    if '-h' in sys.argv:
        help()

    if '-b' in sys.argv:
        backup = True

    if '-m' in sys.argv:
        mark = True

    if '-c' in sys.argv:
        check_file_name = sys.argv[sys.argv.index('-c')+1]

    if '-d' in sys.argv:
        database_file_name = sys.argv[sys.argv.index('-d')+1]

    if '-i' in sys.argv:
        input_file_name = sys.argv[sys.argv.index('-i')+1]

    if '-l' in sys.argv:
        load_value = int(sys.argv[sys.argv.index('-l')+1])

    if '-s' in sys.argv:
        store_value = int(sys.argv[sys.argv.index('-s')+1])

    if '-v' in sys.argv:
        start = time.time()
        verbose = int(sys.argv[sys.argv.index('-v')+1])
        print("Mode: verbose " + str(verbose))
        print("Check file: ", check_file_name)
        print("Backup: ", backup)

    total_new_added = 0
    if '-i' in sys.argv:
        if verbose:
            print("Input file: ", input_file_name, end="\n")


        cd = cdg()
        cd.store_games(pgn_file_name=input_file_name, mark=mark, database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose, backup=backup)

    # VERSIONE ALL
    elif '-a' in sys.argv:
        path = sys.argv[sys.argv.index('-a')+1] + "/*.pgn"
        multiprocessing_option = 0
        if '-p' in sys.argv:
            multiprocessing_option = int(sys.argv[sys.argv.index('-p')+1])

        cd = cdg(multiprocessing_option)

        # carico la prima volta i file
        cd.load_database(database_file_name=database_file_name, verbose=verbose)
        cd.load_check_file(check_file_name=check_file_name, verbose=verbose)

        index = 0
        l = len(glob.glob(path))
        total_new_added = 0
        if verbose:
            print("Loads all in the path: ", path)
            print(f"Loads database and check file each {load_value} file loaded")
            print(f"Store database and check file each {store_value} file loaded")
            if multiprocessing_option:
                print("Multiprocessing " + Fore.GREEN + "ON" + Fore.RESET)

        if not multiprocessing_option:      # multiprocessing off
            for pgn_file in glob.glob(path):
                index += 1

                load = True
                store = True

                if load_value == 0:
                    load = False
                elif index % load_value == 0:
                    load = True
                else:
                    load = False

                if store_value == 0:
                    store = False
                elif index % store_value == 0:
                    store = True
                else:
                    store = False

                added = cd.store_games(pgn_file_name=pgn_file, mark=mark, database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose, backup=backup, load=load, store=store)
                total_new_added += added

                if verbose:
                    print(Fore.RESET + "\nAdded new " + Fore.BLUE + str(added) + Fore.RESET + " games")
                    if index == l:
                        print(Fore.GREEN + f"\nPNG File done: {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET, end="\n")
                    else:
                        print(Fore.LIGHTYELLOW_EX + f"PNG File done: {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET, end="")

            # store database e check file manuale alla fine del ciclo con annesso backup
            cd.store(database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose)

        else:       # multiprocessing on
            if multiprocessing_option <= 0:
                pool = multiprocessing.Pool()
            else:
                pool = multiprocessing.Pool(multiprocessing_option)

            params = []

            try:
                if verbose:
                    print("Generate parameters for multiprocessing... ", end="")

                count = 0
                for pgn_file in glob.glob(path):

                    load = False
                    store = False

                    if load_value == 0:
                        load = False
                    elif count % load_value == 0:
                        load = True
                    else:
                        load = False

                    if store_value == 0:
                        store = False
                    elif count % store_value == 0:
                        store = True
                    else:
                        store = False

                    params.append( (pgn_file, mark, database_file_name, check_file_name, verbose, backup, load, store) )

                if verbose:
                    print(Fore.GREEN + "OK" + Fore.RESET)

            except Exception as e:
                if verbose:
                    print(Fore.RED + "ERROR" + Fore.RESET)

            res = pool.starmap(cd.store_games, params)
            print("res", res)
            # store database e check file manuale alla fine del ciclo con annesso backup
            cd.store(database_file_name=database_file_name, check_file_name=check_file_name, verbose=verbose)


    if verbose:
        end = time.time()
        print("\n\nTotal new added: " + Fore.BLUE + str(total_new_added) + Fore.RESET + " games")
        print(Fore.MAGENTA + "Execution time: ", str(end - start), "s" + Fore.RESET)

    print(Fore.RESET, end="")