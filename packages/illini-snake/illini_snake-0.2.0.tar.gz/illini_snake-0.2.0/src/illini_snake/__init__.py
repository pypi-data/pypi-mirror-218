import json
import os
DIR = os.path.dirname(os.path.abspath( __file__ ))
settings = json.load( open(os.path.join( DIR, 'settings.json' ),'r') )

from .base import Base
from .square import Square
from .food import Food
from .snake import Snake
from .screen import Screen
from . import utils
from .game import Game
