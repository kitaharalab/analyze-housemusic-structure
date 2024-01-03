from external_libraries import *
from modules import *
import data_const as const

def plot_spaghetti(drum_times_all_songs, drum_mapping):
    target_drums = set(['Acoustic Bass Drum', 'Acoustic Snare', 'Closed Hi-Hat'])

    for drum, songs_times in drum_times_all_songs.items():
        if drum not in target_drums:
            continue

        plt.figure(figsize=(10, 6))
        for song, times in songs_times.items():
            times_percentage = [time * 100 for time in times]
            plt.plot(times_percentage, range(len(times)), label=song, marker='o', linestyle='-', markersize=0.01)
        plt.title(f"Drum Events for {drum}")
        plt.xlabel("Time (%)")
        plt.ylabel("Number of Events")
        # plt.legend()
        plt.show()

def process_midi_file_single(midi_path, section_data, drum_mapping, song_length):
    drum = Drum(midi_path)
    drum_events = drum.get_drum_events()
    section_counts = {section['label']: {name: 0 for name in drum_mapping.values()} for section in section_data['segments']}

    existing_drums = set()
    drum_times = {drum_name: [] for drum_name in drum_mapping.values()}
    for note, event in drum_events.items():
        drum_name = event['name']
        existing_drums.add(drum_name)
        normalized_times = [time / song_length for time in event['times']]
        drum_times[drum_name].extend(normalized_times)
        for time in normalized_times:
            for section in section_data['segments']:
                if section['start'] <= time * song_length < section['end']:
                    section_counts[section['label']][drum_name] += 1
                    break

    return section_counts, existing_drums, drum_times

def process_file(json_path, midi_directory, allin1, all_section_counts, all_existing_drums, drum_times_all_songs):
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    midi_path = os.path.join(midi_directory, base_name + '.mid')
    if not os.path.exists(midi_path):
        return

    with open(json_path, 'r') as f:
        section_data = json.load(f)

    song_length = section_data['segments'][-1]['end']

    section_counts, existing_drums, drum_times = process_midi_file_single(midi_path, section_data, Drum(midi_path).drum_mapping, song_length)
    for drum, times in drum_times.items():
        drum_times_all_songs[drum][base_name].extend(times)

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

                progress_bar.update(1)

    progress_bar.close()

    plot_spaghetti(drum_times_all_songs, Drum(midi_directory).drum_mapping)

if __name__ == "__main__":
    main()
