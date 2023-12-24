from external_libraries import *
from modules import *

def main():
    path = '../data/prod/allin1_4_read'

    Allin1.format_json(path)
    Allin1.update_path_json(path)
    Allin1.modify_json(path)
    Allin1.convert_time_format(path)
    # Allin1.revert_time_format(path)

if __name__ == "__main__":
    main()
