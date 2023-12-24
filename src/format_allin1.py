from external_libraries import *

def main():
    path = '../data/demo/allin1_demo'

    Allin1.format_json(path)
    Allin1.update_path_json(path)
    Allin1.modify_json(path)

if __name__ == "__main__":
    main()
