from external_libraries import *
from modules import *
import data_const as const

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
    json_directory = const.PROD_JSON_DIRECTORY
    demucs_directory = const.PROD_DEMUCS_DIRECTORY
    allin1 = Allin1()
    components = ['bass', 'drums', 'other', 'vocals']
    rms_threshold = 0.01
    total_play_times_by_component = {component: {'intro': 0, 'drop': 0, 'break': 0, 'outro': 0} for component in components}

    total_files = sum([len(files) for r, d, files in os.walk(json_directory) if any(file.endswith(".json") for file in files)])
    progress_bar = tqdm(total=total_files, desc="Overall Progress")

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
