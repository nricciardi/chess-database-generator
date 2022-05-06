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
    -v <value> -> verbose (0, 1, 2); default 0
    -a <path>-> all file .pgn in root
    -c <check_file_name> -> use sha control file
    -i <input_file_name> -> input file
    -h -> help
    -b <each x times> -> backup database, 0 is backup off
    -s <store each x times>-> 
    
    default value:
    verbose = 0
    backup = 0
    input_file_name = "input.pgn"
    check_file_name = "check.json"
    store_time = 0'''

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
    # -b <value> -> backup
    # -s <value> -> doesnt store each time

    # default
    verbose = 0
    backup = 0
    store_time = 0
    input_file_name = "input.pgn"
    check_file_name = "check.json"

    if '-h' in sys.argv:
        help()

    if '-b' in sys.argv:
        backup = sys.argv[sys.argv.index('-b')+1]

    if '-s' in sys.argv:
        backup = sys.argv[sys.argv.index('-s')+1]

    if '-c' in sys.argv:
        input_file_name = sys.argv[sys.argv.index('-c')+1]

    if '-i' in sys.argv:
        input_file_name = sys.argv[sys.argv.index('-i')+1]

    if '-v' in sys.argv:
        start = time.time()
        verbose = sys.argv[sys.argv.index('-v')+1]
        print("Input file: ", input_file_name)
        print("Mode: verbose")
        print("Backup: ", backup, end="\n")


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
            cd.load_pgn(pgn_file, verbose)
            cd.store_games(check_file_name=check_file_name, verbose=verbose, backup=backup)

            index += 1

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