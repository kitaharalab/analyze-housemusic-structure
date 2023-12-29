from external_libraries import *
from modules import *

def process_midi_file(midi_path, json_directory, allin1):
    song_name = os.path.splitext(os.path.basename(midi_path))[0]
    json_path = os.path.join(json_directory, f"{song_name}.json")
    section_data = allin1.load_section_data(json_path)

    drum = Drum(midi_path)
    events = drum.get_drum_events()
    pattern_changes = drum.detect_pattern_changes(events)
    drum.plot_drum_with_pattern_and_segments(song_name, events, pattern_changes, section_data)

def main():
    midi_directory = "../data/prod/midi/"
    json_directory = "../data/prod/allin1_formatted/"
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
