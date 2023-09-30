import os
import sys
import mido
from mido import MidiFile, MetaMessage
import pretty_midi

if len(sys.argv) < 2:
    print("Usage: python p.py <midi_file>")
    sys.exit()

input_file = sys.argv[1]
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

# Combine D2 and E2 notes in the same list
# Checking if index 40 exists and is not None in notes_by_pitch
if notes_by_pitch.get(40) is not None:
    # If index 38 doesn't exist, initialize it as an empty list
    if notes_by_pitch.get(38) is None:
        notes_by_pitch[38] = []
    # Extend the notes at index 38 with notes from index 40
    notes_by_pitch[38].extend(notes_by_pitch[40])
    # Clear the notes at index 40
    notes_by_pitch[40] = []

# Iterate through notes by pitch and create separate files
for pitch, notes in notes_by_pitch.items():
    if notes:  # Check if there are notes for this pitch
        # Create a new MIDI file object
        single_note_midi = pretty_midi.PrettyMIDI()
        # Create a drum instrument instance
        single_note_instrument = pretty_midi.Instrument(program=0, is_drum=True)  # Set is_drum to True
        # Append the notes
        single_note_instrument.notes.extend(notes)
        # Always include notes above 51
        single_note_instrument.notes.extend(notes_above_51)
        single_note_midi.instruments.append(single_note_instrument)
        # Write out the MIDI data
        output_filename = f'output_note_{pitch}.mid'
        single_note_midi.write(os.path.join(output_directory, output_filename))

        # Load the output file with mido to change the tempo
        mid = MidiFile(os.path.join(output_directory, output_filename))
        for i, track in enumerate(mid.tracks):
            for j, msg in enumerate(track):
                if msg.type == 'set_tempo':
                    # Set the tempo to 100 BPM
                    tempo = mido.bpm2tempo(100)  # Convert BPM to microseconds per beat
                    track[j] = MetaMessage('set_tempo', tempo=tempo)
        # Save the modified MIDI file
        mid.save(os.path.join(output_directory, output_filename))
