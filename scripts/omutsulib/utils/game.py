import os
from omutsulib.utils.paths import get_sims_documents_directory


def get_game_version():
    game_version_file_path = get_sims_documents_directory() + "GameVersion.txt"
    if os.path.exists(game_version_file_path):
        try:
            with open(game_version_file_path, "rb") as file:
                version_data = file.read()
            if len(version_data) >= 16:
                return version_data[4:].decode()
        except:
            pass

        return "Unknown"


def get_game_version_int():
    game_version_str = get_game_version()
    try:
        if "." in game_version_str:
            game_version_split = game_version_str.split(".")
            if len(game_version_split) == 4:
                return tuple((int(v) for v in game_version_split))
    except:
        pass

    return ()
