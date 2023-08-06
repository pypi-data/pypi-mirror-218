import json
from GustavSelfBot import log

try:
    file = open("config.json")
    Config = json.load(file)
    file.close()
except FileNotFoundError:
    log.error("Config file not found!")
    raise Exception("Config file not found!")

log.info("Config loaded!")
