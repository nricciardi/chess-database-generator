from CDG import ChessDatabaseGenerator as cdg
import time
from colorama import Fore, init
init()
import glob
import sys

def help():
    print(Fore.BLUE + "Chess Database Generator CLI:\n" + Fore.RESET)
    message = '''CDG-cli.py [-flag] <value>
    
    flags:
    -v <level> -> verbose level (0, 1, 2); default 0
    -a <path> -> loads all file .pgn in root
    -c <check_file_name> -> use sha control file
    -i <input_file_name> -> loads only the input file
    -h -> get help
    -b -> backup database and check file each store
    
    # Only for -a:
    -l <value > 0> -> load database and check file each <value> add; 1: each add, ... 
    -s <value > 0> -> store database and check file each <value> add; 1: each add, ... 
'''

    print(message)
    print()

if __name__ == '__main__':

    print(Fore.RESET, end="")

    # CDG-cli.py [-flag] <value>
    # flags:
    # -v <value> -> verbose (0, 1, 2); default 0
    # -a <path> -> all file .pgn in path
    # -c <check_file_name> -> use sha control file
    # -i <input_file_name> -> input file
    # -h -> help
    # -b -> backup

    # default
    verbose = 0
    backup = False
    input_file_name = "input.pgn"
    check_file_name = "check.json"

    if '-h' in sys.argv:
        help()

    if '-b' in sys.argv:
        backup = True

    if '-c' in sys.argv:
        input_file_name = sys.argv[sys.argv.index('-c')+1]

    if '-i' in sys.argv:
        input_file_name = sys.argv[sys.argv.index('-i')+1]

    if '-v' in sys.argv:
        start = time.time()
        verbose = sys.argv[sys.argv.index('-v')+1]
        print("Input file: ", input_file_name)
        print("Mode: verbose\n")


    if '-i' in sys.argv:
        cd = cdg()
        cd.load_pgn(input_file_name, verbose)
        cd.store_games(check_file_name=check_file_name, verbose=verbose, backup=backup)

    elif '-a' in sys.argv:
        path = sys.argv[sys.argv.index('-a')+1] + "/*.pgn"
        cd = cdg()
        index = 0
        l = len(glob.glob(path))
        for pgn_file in glob.glob(path):
            index += 1

            # TODO: verificare se effettuare il load database e check preventivo prima del ciclo in base a load
            # TODO: if di controllo se fare lo store o il load

            cd.load_pgn(pgn_file, verbose)
            cd.store_games(check_file_name=check_file_name, verbose=verbose, backup=backup)

            if verbose:
                print()
                if index == l:
                    print(Fore.GREEN + f"\nPNG File {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET, end="")
                else:
                    print(Fore.LIGHTYELLOW_EX + f"\nPNG File {index}/{l} - {round(100 * index / l, 2)}%" + Fore.RESET, end="")

    if verbose:
        end = time.time()
        print(Fore.MAGENTA + "\n\nExecution time: ", str(end - start), "s" + Fore.RESET)

    print(Fore.RESET, end="")