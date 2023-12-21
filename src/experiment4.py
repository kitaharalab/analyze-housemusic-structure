from external_libraries import *
from modules import *

def load_section_data(json_path: str):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def process_midi_file_single(midi_path, section_data, drum_mapping):
    drum = Drum(midi_path)
    drum_events = drum.get_drum_events()
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

def process_midi_file_combined(midi_path, section_data, drum_mapping, all_section_counts, all_existing_drums):
    drum = Drum(midi_path)
    drum_events = drum.get_drum_events()

    existing_drums = set()
    section_counts = {'intro': {}, 'drop': {}, 'break': {}, 'outro': {}}

    for note, event in drum_events.items():
        drum_name = event['name']
        existing_drums.add(drum_name)
        for time in event['times']:
            for section in section_data['segments']:
                if section['start'] <= time < section['end']:
                    if drum_name in section_counts[section['label']]:
                        section_counts[section['label']][drum_name] += 1
                    else:
                        section_counts[section['label']][drum_name] = 1
                    break

    for section, counts in section_counts.items():
        if section not in all_section_counts:
            all_section_counts[section] = {}
        for drum, count in counts.items():
            if drum in all_section_counts[section]:
                all_section_counts[section][drum] += count
            else:
                all_section_counts[section][drum] = count

    all_existing_drums.update(existing_drums)

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

def main(process_mode):
    json_directory = "../data/demo/allin1_demo/"
    midi_directory = "../data/demo/midi_demo/"

    all_section_counts = {'intro': {}, 'drop': {}, 'break': {}, 'outro': {}}
    all_existing_drums = set()

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

                if process_mode == 'single':
                    section_counts, existing_drums = process_midi_file_single(midi_path, section_data, Drum(midi_path).drum_mapping)
                    plot_drum_section_counts(song_name, section_counts, existing_drums)
                elif process_mode == 'combined':
                    process_midi_file_combined(midi_path, section_data, Drum(midi_path).drum_mapping, all_section_counts, all_existing_drums)

    if process_mode == 'combined':
        num_sections = len(all_section_counts)
        num_cols = 2
        num_rows = np.ceil(num_sections / num_cols).astype(int)
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6 * num_rows))
        axes = axes.flatten()

        for i, (section, counts) in enumerate(all_section_counts.items()):
            if i < len(axes):
                ax = axes[i]
                filtered_counts = {k: v for k, v in counts.items() if k in all_existing_drums}
                ax.bar(range(len(filtered_counts)), list(filtered_counts.values()), tick_label=list(filtered_counts.keys()))
                ax.set_title(f"All Songs - {section} Section")
                ax.set_xlabel("Drum Elements")
                ax.set_ylabel("Counts")
                ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    process_mode = 'combined'  # 'single' or 'combined'
    main(process_mode)
