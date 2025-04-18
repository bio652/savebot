TOKEN = "bot_token"
ADMINS = [
    "admin_tg_id",
]

import json
FILENAME = "channels.json"
def loadchannels():
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            channels = json.load(file)
        return channels
    except FileNotFoundError:
        print(f"{FILENAME} not found")
    except Exception as e:
        print(f"JSON: {e}")
    return {}
def savechannels():
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(channels, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"JSON: {e}")
        return False
        
channels = loadchannels()