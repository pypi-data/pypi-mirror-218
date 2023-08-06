import re
import sqlite3
import time

connection = sqlite3.connect("sqlite3.db")

_global_timer = time.time()
