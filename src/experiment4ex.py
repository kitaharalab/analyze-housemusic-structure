from external_libraries import *
from modules import *
import data_const as const

def plot_spaghetti(drum_times_all_songs, drum_mapping):
    target_drums = set(['Acoustic Bass Drum', 'Acoustic Snare', 'Closed Hi-Hat'])
    common_color = 'blue'
    alpha_value = 0.1

    for drum, songs_times in drum_times_all_songs.items():
        if drum not in target_drums:
            continue

        plt.figure(figsize=(10, 6))
        for song, times in songs_times.items():
            times_sorted = sorted(times)
            plt.plot(times_sorted, range(len(times_sorted)), label=song, marker='o', linestyle='-', markersize=0.01,
                     color=common_color, alpha=alpha_value)
        plt.title(f"Drum Events for {drum}")
        plt.xlabel("Time (s)")
        plt.ylabel("Number of Events")
        plt.tight_layout()
        plt.show()

def process_midi_file(midi_path, section_data, drum_mapping):
    drum = Drum()
    drum_events = drum.get_drum_events(midi_path)
    section_counts = {section['label']: {name: 0 for name in drum_mapping.values()} for section in section_data['segments']}

    existing_drums = set()
    drum_times = {drum_name: [] for drum_name in drum_mapping.values()}
    for note, event in drum_events.items():
        drum_name = event['name']
        existing_drums.add(drum_name)
        drum_times[drum_name].extend(event['times'])
        for time in event['times']:
            for section in section_data['segments']:
                if section['start'] <= time < section['end']:
                    section_counts[section['label']][drum_name] += 1
                    break

    return section_counts, existing_drums, drum_times

def process_file(json_path, midi_directory, allin1, all_section_counts, all_existing_drums, drum_times_all_songs):
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    midi_path = os.path.join(midi_directory, base_name + '.mid')
    if not os.path.exists(midi_path):
        return

    song_name = base_name

    section_data = allin1.load_section_data(json_path)
    section_counts, existing_drums, drum_times = process_midi_file(midi_path, section_data, Drum().drum_mapping)
    for drum, times in drum_times.items():
        drum_times_all_songs[drum][song_name].extend(times)


def main():
    json_directory = const.PROD_JSON_DIRECTORY
    midi_directory = const.PROD_MIDI_DIRECTORY
    allin1 = Allin1()

    all_section_counts = {'intro': {}, 'drop': {}, 'break': {}, 'outro': {}}
    all_existing_drums = set()
    drum_times_all_songs = defaultdict(lambda: defaultdict(list))

    total_files = sum([len(files) for r, d, files in os.walk(json_directory) if any(file.endswith(".json") for file in files)])
    progress_bar = tqdm(total=total_files, desc="Overall Progress")

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                process_file(json_path, midi_directory, allin1, all_section_counts, all_existing_drums, drum_times_all_songs)
                song_name = os.path.splitext(file)[0]
                midi_path = os.path.join(midi_directory, song_name + '.mid')
                if not os.path.exists(midi_path):
                    continue
                section_data = allin1.load_section_data(json_path)
                _, _, drum_times = process_midi_file(midi_path, section_data, Drum().drum_mapping)

                for drum, times in drum_times.items():
                    drum_times_all_songs[drum][song_name].extend(times)

                progress_bar.update(1)

    progress_bar.close()

    plot_spaghetti(drum_times_all_songs, Drum().drum_mapping)

if __name__ == "__main__":
    main()
