from external_libraries import *
from modules import *
import data_const as const

"""
def process_midi_file(midi_path, json_directory, allin1):
    song_name = os.path.splitext(os.path.basename(midi_path))[0]
    json_path = os.path.join(json_directory, f"{song_name}.json")
    section_data = allin1.load_section_data(json_path)

    drum = Drum(midi_path)
    events = drum.get_drum_events()
    pattern_changes = drum.detect_pattern_changes(events)
    # drum.plot_drum_with_pattern_changes(song_name, events, pattern_changes)
    drum.plot_drum_with_pattern_and_sections(song_name, events, pattern_changes,section_data)
"""

def calculate_matching_rate(pattern_changes, section_changes):
    matched_count = 0

    for pattern_change in pattern_changes:
        if any(pattern_change - 1 <= section_change <= pattern_change + 1 for section_change in section_changes):
            matched_count += 1

    matching_rate = (matched_count / len(pattern_changes)) * 100
    return matching_rate

def process_midi_file(midi_path, json_directory, allin1):
    song_name = os.path.splitext(os.path.basename(midi_path))[0]
    json_path = os.path.join(json_directory, f"{song_name}.json")
    section_data = allin1.load_section_data(json_path)

    drum = Drum(midi_path)
    events = drum.get_drum_events()
    pattern_changes = drum.detect_pattern_changes(events)

    section_changes = [int(round(segment['start'])) for segment in section_data['segments']]
    section_changes = sorted(set(section_changes))

    matching_rate = calculate_matching_rate(pattern_changes, section_changes)

    print(f"Song: {song_name}")
    # print("Drum Pattern Changes:", pattern_changes)
    # print("Section Changes:", section_changes)
    print(f"Matching Rate: {matching_rate}%")

    # drum.plot_drum_with_pattern_and_sections(song_name, events, pattern_changes, section_data)


def main():
    midi_directory = const.DEMO_MIDI_DIRECTORY
    json_directory = const.DEMO_JSON_DIRECTORY
    allin1 = Allin1()

    total_files = sum([len(files) for r, d, files in os.walk(midi_directory) if any(file.endswith(".mid") for file in files)])
    progress_bar = tqdm(total=total_files, desc="Overall Progress")

    for root, dirs, files in os.walk(midi_directory):
        for file in files:
            if file.endswith(".mid"):
                midi_path = os.path.join(root, file)
                process_midi_file(midi_path, json_directory, allin1)
                progress_bar.update(1)

    progress_bar.close()

if __name__ == "__main__":
    main()
