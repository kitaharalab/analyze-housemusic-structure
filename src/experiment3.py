from external_libraries import *
from modules import *

def load_section_data(json_path: str):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_section_rms(y, sr, sections):
    rms_values = {}
    for section in sections:
        start_frame = librosa.time_to_samples(section['start'], sr=sr)
        end_frame = librosa.time_to_samples(section['end'], sr=sr)
        rms = librosa.feature.rms(y=y[start_frame:end_frame]).mean()
        if section['label'] not in rms_values:
            rms_values[section['label']] = []
        rms_values[section['label']].append(rms)
    return rms_values

def combine_audio_files(file1_path, file2_path):
    sound1 = AudioSegment.from_file(file1_path)
    sound2 = AudioSegment.from_file(file2_path)
    combined = sound1.overlay(sound2)
    return np.array(combined.get_array_of_samples(), dtype=np.float32) / (2**15)

def calculate_rms_for_part(part, demucs_directory, song_name, section_data):
    if part == 'other':
        other_path = os.path.join(demucs_directory, song_name, 'other.mp3')
        vocals_path = os.path.join(demucs_directory, song_name, 'vocals.mp3')
        y = combine_audio_files(other_path, vocals_path)
        sr = 44100
    else:
        file_path = os.path.join(demucs_directory, song_name, f"{part}.mp3")
        y, sr = librosa.load(file_path, sr=None)

    return calculate_section_rms(y, sr, section_data['segments'])

def find_max_rms(all_rms_values):
    max_rms = 0
    for section in all_rms_values:
        for part in ['bass', 'drums', 'other']:
            max_rms = max(max_rms, max(all_rms_values[section][part]))
    return max_rms

def plot_3d_rms(section, rms_values, max_rms):
    print(f"Plotting section: {section}")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(rms_values['bass'], rms_values['drums'], rms_values['other'])
    ax.set_xlabel('Bass RMS')
    ax.set_ylabel('Drums RMS')
    ax.set_zlabel('Other RMS')
    ax.set_xlim([0, max_rms])
    ax.set_ylim([0, max_rms])
    ax.set_zlim([0, max_rms])
    ax.set_title(f"Section: {section}")
    plt.show()

def main():
    json_directory = "../data/demo/allin1_demo/"
    demucs_directory = "../data/demo/demucs_demo/mdx_q/"
    all_rms_values = {}
    song_section_rms = {}

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                section_data = load_section_data(json_path)

                song_name = os.path.splitext(file)[0]
                print(f"Processing song: {song_name}")

                song_rms_values = {'bass': {}, 'drums': {}, 'other': {}}
                for part in song_rms_values:
                    rms = calculate_rms_for_part(part, demucs_directory, song_name, section_data)
                    for label, values in rms.items():
                        if label not in all_rms_values:
                            all_rms_values[label] = {'bass': [], 'drums': [], 'other': []}
                            song_section_rms[label] = []
                        all_rms_values[label][part].append(np.mean(values))
                        song_section_rms[label].append(f"Song: {song_name}, Section: {label}, Part: {part}, RMS: {np.mean(values)}")

    max_rms = find_max_rms(all_rms_values)

    for section, rms_values in all_rms_values.items():
        for log_message in song_section_rms[section]:
            print(log_message)
        plot_3d_rms(section, rms_values, max_rms)

if __name__ == "__main__":
    main()
