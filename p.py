import os
import sys
import mido
from mido import MidiFile, MetaMessage
import pretty_midi
import shutil

if len(sys.argv) < 2:
    print("Usage: python p.py <midi_directory>")
    sys.exit()

input_directory = sys.argv[1]

for filename in os.listdir(input_directory):
    if filename.endswith(".mid") or filename.endswith(".midi"):  # Check if it's a MIDI file
        input_file = os.path.join(input_directory, filename)
        midi_data = pretty_midi.PrettyMIDI(input_file)
        
        for instrument in midi_data.instruments:
            instrument.is_drum = True

        filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        words = filename_without_extension.split('_')

        if len(words) == 2:
            first_word, second_word = words
            output_directory = os.path.join(os.getcwd(), first_word, second_word)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
        else:
            print(f"The filename does not contain exactly one underscore.")
            sys.exit()

        source_dir = 'empty'
        all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        for file in all_files[:5]:
            shutil.copy(os.path.join(source_dir, file), output_directory)
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.pitch == 47:
                    note.pitch = 43
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.pitch == 50:
                    note.pitch = 45
        output_file = 'modified_' + os.path.basename(input_file)
        midi_data.write(output_file)

        mid = MidiFile(output_file)
        for i, track in enumerate(mid.tracks):
            for j, msg in enumerate(track):
                if msg.type == 'set_tempo':
                    tempo = mido.bpm2tempo(100)
                    track[j] = MetaMessage('set_tempo', tempo=tempo)

        output_path = os.path.join(output_directory, os.path.basename(input_file))
        mid.save(output_path)

        # Create a dictionary to store notes by pitch
        notes_by_pitch = {}

        # Store notes above 51 to keep them in every file
        notes_above_51 = []

        # Iterate through instrument notes and group by pitch
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.pitch > 51:
                    notes_above_51.append(note)
                if note.pitch not in notes_by_pitch:
                    notes_by_pitch[note.pitch] = []
                notes_by_pitch[note.pitch].append(note)
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.pitch == 47:
                    note.pitch = 43
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                if note.pitch == 50:
                    note.pitch = 45


        # Combine D2 and E2 notes in the same list
        if notes_by_pitch.get(40) is not None:
            if notes_by_pitch.get(38) is None:
                notes_by_pitch[38] = []
            notes_by_pitch[38].extend(notes_by_pitch[40])
            notes_by_pitch[40] = []

        # Iterate through notes by pitch and create separate files
        for pitch, notes in notes_by_pitch.items():
            if notes:
                single_note_midi = pretty_midi.PrettyMIDI()
                single_note_instrument = pretty_midi.Instrument(program=0, is_drum=True)
                single_note_instrument.notes.extend(notes)
                single_note_instrument.notes.extend(notes_above_51)
                single_note_midi.instruments.append(single_note_instrument)
                output_filename = f'output_note_{pitch}.mid'
                single_note_midi.write(os.path.join(output_directory, output_filename))

                mid = MidiFile(os.path.join(output_directory, output_filename))
                for i, track in enumerate(mid.tracks):
                    for j, msg in enumerate(track):
                        if msg.type == 'set_tempo':
                            tempo = mido.bpm2tempo(100)
                            track[j] = MetaMessage('set_tempo', tempo=tempo)
                mid.save(os.path.join(output_directory, output_filename))
