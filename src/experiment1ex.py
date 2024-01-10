from experiment1 import Allin1, plot_bar_graph, plot_box_plot, plot_violin_plot, calculate_section_averages
from external_libraries import *
from modules import *
import data_const as const

def get_rms(file_path):
    y, sr = librosa.load(file_path)
    rms = librosa.feature.rms(y=y)
    times = librosa.times_like(rms)
    return rms, sr, times

def process_file(json_path, song_directory, all_section_averages, allin1):
    section_data = allin1.load_section_data(json_path)

    filename = os.path.splitext(os.path.basename(json_path))[0] + '.mp3'
    file_path = os.path.join(song_directory, filename)
    rms_values, sr, times = get_rms(file_path)
    section_averages = calculate_section_averages(section_data['segments'], rms_values, sr, times)

    for section, average in section_averages.items():
        all_section_averages[section].append(average)

def process_files(json_directory, song_directory, allin1, all_section_averages):
    for root, dirs, files in tqdm(os.walk(json_directory), desc="Processing files"):
        for file in tqdm(files, desc="Overall Progress", leave=False):
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                process_file(json_path, song_directory, all_section_averages, allin1)

def main(process_mode):
    song_directory = const.PROD_SONG_DIRECTORY
    json_directory = const.PROD_JSON_DIRECTORY
    allin1 = Allin1()
    all_section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}

    process_files(json_directory, song_directory, allin1, all_section_averages)

    if process_mode == 'bar':
        plot_bar_graph(all_section_averages)
    elif process_mode == 'box':
        plot_box_plot(all_section_averages)
    elif process_mode == 'violin':
        plot_violin_plot(all_section_averages)

if __name__ == "__main__":
    process_mode = 'box'  # 'bar', 'box', or 'violin'
    main(process_mode)
