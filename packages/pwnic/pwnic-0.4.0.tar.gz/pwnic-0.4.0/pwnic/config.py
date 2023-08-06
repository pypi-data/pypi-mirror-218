TEAM_ID: int = 39
HIGHEST_ID: int = 43
TEAM_TOKEN: str = "bac02cf066bdaae77fab93dd1544ea42"
WARNING_TIME: int = 90  # after WARNING_TIME seconds a warning will be logged
ROUND_DURATION = 120  # in seconds
FLAG_REGEX = r"[A-Z0-9]{31}="
IP_BASE = "10.60.{id}.1"
DB_URL = "mongodb://mongo-milkman:27017/"

WAIT_GAMESTART = True
PING_BEFORE_EXPLOIT = False
CHECK_STATUS = False


def has_game_started() -> bool:  # IMPLEMENT THIS IF WAIT_GAMESTART IS TRUE
    return True
