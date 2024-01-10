from external_libraries import *
from modules import *
import data_const as const
from experiment2 import plot_bar_graph, plot_combined_bar_graph, plot_box_plot, plot_violin_plot, plot_combined_box_plot, plot_combined_violin_plot

def get_rms(file_path):
    y, sr = librosa.load(file_path)
    rms = librosa.feature.rms(y=y)
    times = librosa.times_like(rms, sr=sr)
    return rms, sr, times

def calculate_section_averages(sections, feature_values, sr, times):
    section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}
    feature_values = feature_values.flatten()

    for section in sections:
        label = section['label']
        if label in section_averages:
            start_index = np.argmax(times >= section['start'])
            end_index = np.argmax(times >= section['end'])
            if end_index == 0:
                end_index = len(feature_values)

            section_centroid = feature_values[start_index:end_index]
            if len(section_centroid) > 0:
                section_average = section_centroid.mean()
                section_averages[label].append(section_average)

    for label in section_averages:
        if section_averages[label]:
            section_averages[label] = sum(section_averages[label]) / len(section_averages[label])
        else:
            section_averages[label] = None

    return section_averages

def process_file(json_path, song_directory, component_averages, allin1, components):
    section_data = allin1.load_section_data(json_path)
    song_name = os.path.splitext(os.path.basename(json_path))[0]

    for component in components:
        file_path = os.path.join(song_directory, song_name, f"{component}.mp3")
        if os.path.exists(file_path):
            rms, sr, times = get_rms(file_path)
            section_averages = calculate_section_averages(section_data['segments'], rms, sr, times)

            for section, average in section_averages.items():
                if average is not None:
                    component_averages[component][section].append(average)

def process_files(json_directory, song_directory, allin1, component_averages, components):
    for root, dirs, files in tqdm(os.walk(json_directory), desc="Processing files"):
        for file in tqdm(files, desc="Overall Progress", leave=False):
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                process_file(json_path, song_directory, component_averages, allin1, components)

def main(process_mode):
    song_directory = const.PROD_SONG_DIRECTORY
    json_directory = const.PROD_JSON_DIRECTORY
    demucs_directory = const.PROD_DEMUCS_DIRECTORY
    allin1 = Allin1()

    components = ['bass', 'drums', 'other', 'vocals']
    component_averages = {component: {'intro': [], 'drop': [], 'break': [], 'outro': []} for component in components}

    process_files(json_directory, demucs_directory, allin1, component_averages, components)

    if process_mode == 'bar':
        for component in components:
            plot_bar_graph(component_averages[component], f"Bar Graph for {component.capitalize()}")
    elif process_mode == 'combined_bar':
        plot_combined_bar_graph(component_averages, components)
    elif process_mode == 'box':
        for component in components:
            plot_box_plot(component_averages[component], f"Box Plot for {component.capitalize()}")
    elif process_mode == 'combined_box':
        plot_combined_box_plot(component_averages, components)
    elif process_mode == 'violin':
        for component in components:
            plot_violin_plot(component_averages[component], f"Violin Plot for {component.capitalize()}")
    elif process_mode == 'combined_violin':
        plot_combined_violin_plot(component_averages, components)

if __name__ == "__main__":
    process_mode = 'combined_box'  # 'bar' | 'combined_bar' | 'box' | 'combined_box' | 'violin' | 'combined_violin' | 'rms_plot'
    main(process_mode)
