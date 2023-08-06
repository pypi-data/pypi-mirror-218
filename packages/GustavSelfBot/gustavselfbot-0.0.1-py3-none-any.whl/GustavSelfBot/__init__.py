"""
My self bot!
"""

__version__ = "0.0.1"

from GustavSelfBot.__logging__ import *
from GustavSelfBot.__config__ import Config
from GustavSelfBot.__bot__ import bot

log.info("Main module loaded!")

if Config['token'] == "":
    log.error("No token provided!")
    raise Exception("No token provided!")
