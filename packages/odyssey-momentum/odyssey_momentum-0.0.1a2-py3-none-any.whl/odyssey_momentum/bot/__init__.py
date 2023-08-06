"""
Library to help write bots for momentum.

Bots can automate tasks normal users can do.

It is a higher level, stateful, wrapper around the low level posbus and api clients.
It provides an abstaction of a single user you can order around to do stuff.

"""
# isort: skip_file
from .coords import Position, Rotation
from .world import World
from .user import User
from .bot import Bot
