from external_libraries import *
from modules import *

def get_time_signature_from_midi(file_path):
    midi_file = MidiFile(file_path)
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'time_signature':
                numerator = msg.numerator   # 分子（拍子の数）
                denominator = msg.denominator # 分母（1小節あたりの拍の長さ）
                print(f"Track: {track.name}, Time Signature: {numerator}/{denominator}")

def get_tempo_from_midi(file_path):
    midi_file = MidiFile(file_path)
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = mido.tempo2bpm(msg.tempo)
                print(f"Track: {track.name}, Tempo: {tempo} BPM")



get_tempo_from_midi('../data/demo/midi_demo/01 - My Paradise.mid')
get_time_signature_from_midi('../data/demo/midi_demo/01 - My Paradise.mid')

drum = Drum('../data/demo/midi_demo/01 - My Paradise.mid')
drum.plot_drum_with_measure_lines()
