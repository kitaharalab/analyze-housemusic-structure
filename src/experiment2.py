from external_libraries import *
from modules import *

def load_section_data(json_path: str):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_section_averages(sections, spectral_centroid, sr, times):
    section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}
    spectral_centroid = spectral_centroid.flatten()

    for section in sections:
        label = section['label']
        if label in section_averages:
            start_index = np.argmax(times >= section['start'])
            end_index = np.argmax(times >= section['end'])
            if end_index == 0:
                end_index = len(spectral_centroid)

            section_centroid = spectral_centroid[start_index:end_index]
            if len(section_centroid) > 0:
                section_average = section_centroid.mean()
                section_averages[label].append(section_average)

    for label in section_averages:
        if section_averages[label]:
            section_averages[label] = sum(section_averages[label]) / len(section_averages[label])
        else:
            section_averages[label] = None

    return section_averages

def main():
    song_directory = "../data/demo/songs_demo/"
    demucs_directory = "../data/demo/demucs_demo/mdx_q/"
    json_directory = "../data/demo/allin1_demo/"
    freq = Frequency()

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                section_data = load_section_data(json_path)

                song_name = os.path.splitext(file)[0]
                components = ['bass', 'drums', 'other', 'vocals']

                for component in components:
                    file_path = os.path.join(demucs_directory, song_name, f"{component}.mp3")
                    print(file_path)
                    if os.path.exists(file_path):
                        spectral_centroid, sr, times = freq.get_spectral_centroid(file_path)
                        section_averages = calculate_section_averages(section_data['segments'], spectral_centroid, sr, times)

                        print(f"File: {song_name}, Component: {component}")
                        for section, average in section_averages.items():
                            print(f"Section: {section}, Average Spectral Centroid: {average}")
                    else:
                        print(f"Component file not found: {file_path}")


if __name__ == "__main__":
    main()
