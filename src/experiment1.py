from external_libraries import *
from modules import *
import data_const as const

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

def plot_violin_plot(section_averages):
    data_to_plot = [avgs for avgs in section_averages.values() if avgs]
    plt.violinplot(data_to_plot)
    plt.xticks(range(1, len(section_averages) + 1), section_averages.keys())
    plt.xlabel('Section')
    plt.ylabel('Average Spectral Centroid')
    plt.title('Violin Plot of Average Spectral Centroid per Music Section')
    plt.show()

def process_file(json_path, song_directory, freq, all_section_averages, allin1):
    section_data = allin1.load_section_data(json_path)

    filename = os.path.splitext(os.path.basename(json_path))[0] + '.mp3'
    file_path = os.path.join(song_directory, filename)
    spectral_centroid, sr, times = freq.get_spectral_centroid(file_path)
    section_averages = calculate_section_averages(section_data['segments'], spectral_centroid, sr, times)

    for section, average in section_averages.items():
        all_section_averages[section].append(average)

def process_files(json_directory, song_directory, freq, allin1, all_section_averages):
    for root, dirs, files in tqdm(os.walk(json_directory), desc="Processing files"):
        for file in tqdm(files, desc="Processing file", leave=False):
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                process_file(json_path, song_directory, freq, all_section_averages, allin1)

def main(process_mode):
    song_directory = const.DEMO_SONG_DIRECTORY
    json_directory = const.DEMO_JSON_DIRECTORY
    freq = Frequency()
    allin1 = Allin1()
    all_section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}

    process_files(json_directory, song_directory, freq, allin1, all_section_averages)

    if process_mode == 'var':
        plot_bar_graph(all_section_averages)
    elif process_mode == 'box':
        plot_box_plot(all_section_averages)
    elif process_mode == 'violin':
        plot_violin_plot(all_section_averages)

if __name__ == "__main__":
    process_mode = 'violin'  # 'var', 'box', or 'violin'
    main(process_mode)
