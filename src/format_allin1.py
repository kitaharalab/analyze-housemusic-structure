from external_libraries import *

class Allin1:
    @classmethod
    def format_json(cls, path):
        json_files = [file for file in os.listdir(path) if file.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(path, json_file)

            with open(file_path, 'r') as file:
                data = json.load(file)

            for item in list(data.keys()):
                if item not in ('path', 'segments'):
                    del data[item]

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"{colored('format_json', 'blue')}: Update '{json_file}'.")

        print("All json files have been updated.")

    @classmethod
    def update_path_json(cls, path):
        json_files = [file for file in os.listdir(path) if file.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(path, json_file)

            with open(file_path, 'r') as file:
                data = json.load(file)

            data['path'] = file_path

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"{colored('update_path_json', 'blue')}: Update path of '{json_file}'.")

        print("All json files have been updated.")

    @classmethod
    def modify_label(cls, label):
        label_mappings = {
                'start': 'intro',
                'end': 'outro',
                'bridge': 'break',
                'inst': 'break',
                'solo': 'break',
                'verse': 'break',
                'chorus': 'drop'
                }
        return label_mappings.get(label, label)

    @classmethod
    def modify_json(cls, path):
        json_files = [file for file in os.listdir(path) if file.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(path, json_file)

            with open(file_path, 'r') as file:
                data = json.load(file)

            if 'segments' in data and isinstance(data['segments'], list):
                for segment in data['segments']:
                    if 'label' in segment:
                        segment['label'] = cls.modify_label(segment['label'])

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"{colored('modify_json', 'blue')}: Modified '{json_file}'.")

        print("All json files have been modified.")


def main():
    path = '../data/demo/allin1_demo'

    Allin1.format_json(path)
    Allin1.update_path_json(path)
    Allin1.modify_json(path)

if __name__ == "__main__":
    main()
