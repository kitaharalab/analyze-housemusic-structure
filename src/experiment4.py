from external_libraries import *
from modules import *

def load_section_data(json_path: str):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def process_midi_file(midi_path, section_data, drum_mapping):
    visualizer = DrumMidiVisualizer(midi_path)
    drum_events = visualizer.get_drum_events()
    section_counts = {section['label']: {name: 0 for name in drum_mapping.values()} for section in section_data['segments']}

    existing_drums = set()
    for note, event in drum_events.items():
        drum_name = event['name']
        existing_drums.add(drum_name)
        for time in event['times']:
            for section in section_data['segments']:
                if section['start'] <= time < section['end']:
                    section_counts[section['label']][drum_name] += 1
                    break

    return section_counts, existing_drums

def plot_drum_section_counts(song_name, section_counts, existing_drums):
    num_sections = len(section_counts)
    num_cols = 2
    num_rows = np.ceil(num_sections / num_cols).astype(int)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, (section, counts) in enumerate(section_counts.items()):
        if i < len(axes):
            ax = axes[i]
            filtered_counts = {k: v for k, v in counts.items() if k in existing_drums}
            ax.bar(range(len(filtered_counts)), list(filtered_counts.values()), tick_label=list(filtered_counts.keys()))
            ax.set_title(f"{song_name} - {section} Section")
            ax.set_xlabel("Drum Elements")
            ax.set_ylabel("Counts")
            ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def main():
    json_directory = "../data/demo/allin1_demo/"
    midi_directory = "../data/demo/midi_demo/"

    for root, dirs, files in os.walk(json_directory):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                midi_path = os.path.join(midi_directory, os.path.splitext(file)[0] + '.mid')
                if not os.path.exists(midi_path):
                    continue

                song_name = os.path.splitext(file)[0]
                print(f"Processing song: {song_name}")
                section_data = load_section_data(json_path)
                visualizer = DrumMidiVisualizer(midi_path)
                section_counts, existing_drums = process_midi_file(midi_path, section_data, visualizer.drum_mapping)
                plot_drum_section_counts(song_name, section_counts, existing_drums)

if __name__ == "__main__":
    main()
