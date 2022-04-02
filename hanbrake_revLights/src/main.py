import sys
from UDPRecievers import forzaUDP, pc2UDP


def main(args):
    """main func

    Parameters
    ----------
    args tuple: 
        command line args
    """

    print("Program started!")

    game = 0

    # select the game
    while game not in (1,2):
        game = int(input("Please select the game:\n1 - Forza Horizon 4/5\n2 - Project Cars 1/2\n\n>>>"))
        if game not in (1,2):
            print("ERROR: Invalid choice.")

    # run with forza compatibility
    if game == 1:
        forzaUDP()

    # run with project cars 2 compatibility
    else:
        pc2UDP()

    

if __name__ == '__main__':
    main(sys.argv)