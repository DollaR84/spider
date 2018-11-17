"""
Main module for running spider game.

Created on 17.11.2018

@author: Ruslan Dolovanyuk

"""

import multiprocessing

from game import Game

if __name__ == '__main__':
    multiprocessing.freeze_support()
    game = Game()
    game.mainloop()
