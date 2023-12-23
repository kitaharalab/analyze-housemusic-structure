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
        start_index = np.argmax(times >= section['start'])
        end_index = np.argmax(times >= section['end'])
        if end_index == 0:
            end_index = len(spectral_centroid)
        section_centroid = spectral_centroid[start_index:end_index]
        if len(section_centroid) > 0:
            section_averages[label].append(section_centroid.mean())

    section_averages_mean = {}
    for label, values in section_averages.items():
        if values:
            section_averages_mean[label] = np.mean(values)

    return section_averages_mean

def plot_bar_graph(section_averages):
    total_averages = {}
    for section, avgs in section_averages.items():
        if avgs:
            total_averages[section] = np.mean(avgs)

    plt.bar(total_averages.keys(), total_averages.values(), alpha=0.5, label='Average per section')
    for section, avgs in section_averages.items():
        if avgs:
            plt.scatter([section] * len(avgs), avgs, color='red', label='Individual averages' if section == 'intro' else "")

    plt.xlabel('Section')
    plt.ylabel('Average Spectral Centroid')
    plt.title('Average Spectral Centroid per Music Section')
    plt.legend()
    plt.show()

def plot_box_plot(section_averages):
    plt.boxplot(section_averages.values(), labels=section_averages.keys())
    plt.xlabel('Section')
    plt.ylabel('Average Spectral Centroid')
    plt.title('Box Plot of Average Spectral Centroid per Music Section')
    plt.show()

def main(process_mode):
    song_directory = "../data/demo/songs_demo/"
    json_directory = "../data/demo/allin1_demo/"
    freq = Frequency()
    all_section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                section_data = load_section_data(json_path)

                filename = os.path.splitext(file)[0] + '.mp3'
                file_path = os.path.join(song_directory, filename)
                spectral_centroid, sr, times = freq.get_spectral_centroid(file_path)
                section_averages = calculate_section_averages(section_data['segments'], spectral_centroid, sr, times)

                for section, average in section_averages.items():
                    all_section_averages[section].append(average)

    if process_mode == 'var':
        plot_bar_graph(all_section_averages)
    elif process_mode == 'box':
        plot_box_plot(all_section_averages)

if __name__ == "__main__":
    process_mode = 'box'  # 'var' or 'box'
    main(process_mode)
