
import vhcs.common.util as util
from os import path

_template_dir = path.abspath(path.join(path.dirname(__file__), "templates"))

def get(name: str):
    file_name = path.join(_template_dir, name)
    return util.load_data_file(file_name)

