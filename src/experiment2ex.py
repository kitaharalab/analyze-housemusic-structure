from external_libraries import *
from modules import *
import data_const as const

def process_files(json_directory, song_directory, freq, allin1, component_averages, components):
    for root, dirs, files in tqdm(os.walk(json_directory), desc="Processing files"):
        for file in tqdm(files, desc="Processing file", leave=False):
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                process_file(json_path, song_directory, freq, component_averages, allin1, components)

def process_file(json_path, song_directory, freq, component_averages, allin1, components):
    section_data = allin1.load_section_data(json_path)
    song_name = os.path.splitext(os.path.basename(json_path))[0]

    for component in components:
        file_path = os.path.join(song_directory, song_name, f"{component}.mp3")
        if os.path.exists(file_path):
            spectral_centroid, sr, times = freq.get_spectral_centroid(file_path)
            section_averages = calculate_filtered_section_averages(
                section_data['segments'], spectral_centroid, sr, times, file_path)

            for section, average in section_averages.items():
                if average is not None:
                    component_averages[component][section].append(average)

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

def calculate_filtered_section_averages(sections, spectral_centroid, sr, times, audio_path, rms_threshold=0.01):
    y, _ = librosa.load(audio_path, sr=None)
    section_averages = {'intro': [], 'drop': [], 'break': [], 'outro': []}
    spectral_centroid = spectral_centroid.flatten()

    for section in sections:
        label = section['label']
        if label in section_averages:
            start_index = np.argmax(times >= section['start'])
            end_index = np.argmax(times >= section['end'])
            if end_index == 0:
                end_index = len(spectral_centroid)

            valid_indices = filter_by_rms(y, sr, start_index, end_index, rms_threshold)
            filtered_centroid = spectral_centroid[start_index:end_index][valid_indices]

            if len(filtered_centroid) > 0:
                section_average = filtered_centroid.mean()
                section_averages[label].append(section_average)

    for label in section_averages:
        if section_averages[label]:
            section_averages[label] = sum(section_averages[label]) / len(section_averages[label])
        else:
            section_averages[label] = None

    return section_averages

def filter_by_rms(y, sr, start_index, end_index, rms_threshold):
    rms = librosa.feature.rms(y=y)[0]
    section_rms = rms[start_index:end_index]
    valid_indices = section_rms >= rms_threshold
    return valid_indices

def calculate_filtered_play_time_by_section_and_component(sections, y, sr, rms_threshold):
    section_play_time = {'intro': 0, 'drop': 0, 'break': 0, 'outro': 0}

    for section in sections:
        label = section['label']
        valid_indices = filter_by_rms(y, sr, section['start'], section['end'], rms_threshold)
        play_time = np.sum(valid_indices) / sr
        section_play_time[label] += play_time

    return section_play_time

def filter_by_rms(y, sr, start_time, end_time, rms_threshold):
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    start_index = np.argmax(times >= start_time)
    end_index = np.argmax(times >= end_time)
    if end_index == 0:
        end_index = len(rms)
    valid_indices = rms[start_index:end_index] >= rms_threshold
    return valid_indices

def plot_stack_bar(total_play_times_by_component):
    sections = ['intro', 'drop', 'break', 'outro']
    components = total_play_times_by_component.keys()

    play_times = {component: [total_play_times_by_component[component][section] for section in sections] for component in components}

    fig, ax = plt.subplots()
    bottom = np.zeros(len(components))
    colors = ['yellow', 'red', 'green', 'blue']

    for i, section in enumerate(sections):
        play_time = np.array([play_times[component][sections.index(section)] for component in components])
        ax.bar(components, play_time, bottom=bottom, label=section.capitalize(), color=colors[i])
        bottom += play_time

    ax.set_xlabel('Component')
    ax.set_ylabel('Total Play Time (Seconds)')
    ax.set_title('Total Play Time by Component and Section')
    ax.legend()

    plt.tight_layout()
    plt.show()

def process_file_for_play_time(json_path, song_directory, allin1, components, rms_threshold):
    section_data = allin1.load_section_data(json_path)
    song_name = os.path.splitext(os.path.basename(json_path))[0]
    component_play_times = {component: {'intro': 0, 'drop': 0, 'break': 0, 'outro': 0} for component in components}

    for component in components:
        file_path = os.path.join(song_directory, song_name, f"{component}.mp3")
        if os.path.exists(file_path):
            y, sr = librosa.load(file_path, sr=None)
            section_play_time = calculate_filtered_play_time_by_section_and_component(section_data['segments'], y, sr, rms_threshold)
            for section, time in section_play_time.items():
                component_play_times[component][section] += time

    return component_play_times

def main(process_mode):
    json_directory = const.DEMO_JSON_DIRECTORY
    demucs_directory = const.DEMO_DEMUCS_DIRECTORY
    allin1 = Allin1()
    components = ['bass', 'drums', 'other', 'vocals']
    rms_threshold = 0.01
    total_play_times_by_component = {component: {'intro': 0, 'drop': 0, 'break': 0, 'outro': 0} for component in components}

    total_files = sum([len(files) for r, d, files in os.walk(json_directory) if any(file.endswith(".json") for file in files)])
    progress_bar = tqdm(total=total_files, desc="Processing files")

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                play_times = process_file_for_play_time(json_path, demucs_directory, allin1, components, rms_threshold)
                for component, times in play_times.items():
                    for section, time in times.items():
                        total_play_times_by_component[component][section] += time
                progress_bar.update(1)

    progress_bar.close()

    if process_mode == 'stack_bar':
        plot_stack_bar(total_play_times_by_component)

if __name__ == "__main__":
    process_mode = 'stack_bar'
    main(process_mode)
