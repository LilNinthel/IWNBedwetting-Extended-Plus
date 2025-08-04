import os, json
from json.decoder import JSONDecodeError
import services
from sims4.resources import Types, get_resource_key
from zone import Zone
from sims.sim_info_types import Species
from sims.sim_info import SimInfo
from sims.aging.aging_element import AgeUpBaby
import sims4.log

def get_iwnbedwetting_save_directory():
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
    root_file_split = root_file.split(os.sep)
    root_dir = str(os.sep).join(root_file_split[0:root_file_split.index("Mods")]) + os.sep + "saves" + os.sep + "IWNBedwetting" + os.sep
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir

def _create_empty_json_settings(filename, data=None):
    save_directory = get_iwnbedwetting_save_directory()
    try:
        with open((os.path.join(save_directory, filename)), buffering=1, encoding="utf-8") as file:
            try:
                data = json.load(file)
                return
            except JSONDecodeError:
                pass

    except FileNotFoundError:
        pass

    if data is None:
        data = {}
    with open((os.path.join(save_directory, filename)), "w", buffering=1, encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)

# _create_empty_json_settings("iwnbedwetting_global_settings.json")

def write_to_settings(filename, data):
    save_directory = get_iwnbedwetting_save_directory()
    with open((os.path.join(save_directory, filename)), "w", buffering=1, encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)


def _write_to_settings(filename, data):
    save_directory = get_iwnbedwetting_save_directory()
    with open((os.path.join(save_directory, filename)), "w+", buffering=1, encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=True)


def read_from_settings(filename):
    save_directory = get_iwnbedwetting_save_directory()
    with open((os.path.join(save_directory, filename)), buffering=1, encoding="utf-8") as file:
        data = json.load(file)
        if data:
            return data
    return False


def get_setting(filename, save_guid, key):
    save_directory = get_iwnbedwetting_save_directory()
    with open((os.path.join(save_directory, filename)), buffering=1, encoding="utf-8") as file:
        data = json.load(file)
        if data:
            if str(save_guid) in data:
                return data[str(save_guid)][key]
    return False


def change_value(filename, save_guid, key, value):
    save_directory = get_iwnbedwetting_save_directory()
    with open((os.path.join(save_directory, filename)), buffering=1, encoding="utf-8") as file:
        data = json.load(file)
        if data:
            if str(save_guid) in data:
                data[str(save_guid)][key] = value
            with open((os.path.join(save_directory, filename)), "w+", buffering=1, encoding="utf-8") as f:
                json.dump(data, f, indent=4, sort_keys=True)
    return False
