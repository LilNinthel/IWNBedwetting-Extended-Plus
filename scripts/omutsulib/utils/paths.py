import enum, os

def get_sims_documents_directory():
    file_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, "/")
    lowercase_file_path_segments = file_path.lower().split("/")
    file_path_segments = file_path.split("/")
    root_segment_index = lowercase_file_path_segments.index("mods")
    root_dir = os.sep.join(file_path_segments[:root_segment_index]) + os.sep
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir


def get_sims_mods_directory():
    mods_dir_path = "{}Mods{}".format(get_sims_documents_directory(), os.sep)
    if not os.path.exists(mods_dir_path):
        os.makedirs(mods_dir_path)
    return mods_dir_path


def get_sims_game_directory():
    file_path = os.path.normpath(os.path.dirname(os.path.realpath(enum.__file__))).replace(os.sep, "/")
    file_path_segments = file_path.split("/")
    root_dir = os.sep.join(file_path_segments[:4]) + os.sep
    return root_dir
