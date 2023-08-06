"""
Package to use the Odyssey momentum (websocket) posbus protocol.

This wraps a python c extensions to read/write the custom protocol.
"""
from .auth import Auth, authenticate_guest, authenticate_web3, web3_account
from .protocol import *  # noqa
from .transport import connect, SendFunc, InGenerator
