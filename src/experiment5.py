from external_libraries import *
from modules import *

def main():
    midi_directory = "../data/demo/midi_demo/"
    json_directory = "../data/demo/allin1_demo/"
    allin1 = Allin1()

    for root, dirs, files in os.walk(midi_directory):
        for file in files:
            if file.endswith(".mid"):
                midi_path = os.path.join(root, file)
                song_name = os.path.splitext(file)[0]
                print(f"Processing song: {song_name}")

                # Load JSON data for the current song
                json_path = os.path.join(json_directory, f"{song_name}.json")
                section_data = allin1.load_section_data(json_path)

                drum = Drum(midi_path)
                events = drum.get_drum_events()
                pattern_changes = drum.detect_pattern_changes(events)
                print(f"Pattern Changes for {song_name}:\n {pattern_changes}")

                drum.plot_drum_with_pattern_and_segments(song_name, events, pattern_changes, section_data)

if __name__ == "__main__":
    main()
