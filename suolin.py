## coding: utf-8
## suolin.py

## Import standard modules
import os
import sys
import time
import logging
import threading

## Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='laster.log', filemode='w')


## Import necessary modules
try:
    from rich.console import Console
    import curses
except ImportError:
    logger.error("necessary module missing.", exc_info=True)
    print("[ERROR]: Some important modules are missing. Please run 'pip install -r requirements.txt' to install them.For more information, please refer to the logs in the program directory.")
    sys.exit(1)
## Initialize the console
console = Console()

## Import internal modules
try:
    import readFile
    import langToLocal
    import setting
except ImportError:
    console.print("[bold red][ERROR][/bold red]: some internal modules are missing. Please try fix this or reinstall the application.For more information, please refer to the logs in the program directory.")
    logger.error("Internal modules missing", exc_info=True)
    sys.exit(1)

def load_config() -> dict:#load config.json
    try:
        config = readFile.LoadJson("config.json")
    except FileNotFoundError:
        logger.warning("config.json not found or corrupted.")
        readFile.fix_config()
        config = readFile.LoadJson("config.json")
    if config["logLevel"] == "INFO":#set log level
        logger.setLevel(logging.INFO)
    elif config["logLevel"] == "WARNING":
        logger.setLevel(logging.WARNING)
    return config


def main(stdscr):
    config = load_config()
    # Further implementation of the main application logic goes here.
    stdscr.addstr(0, 0, "Suolin Application Running...")
    stdscr.refresh()
    stdscr.getkey()
    
if __name__ == "__main__":
    config = load_config()
    curses.wrapper(main)