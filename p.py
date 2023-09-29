import pretty_midi
import os

# Load the MIDI file
midi_data = pretty_midi.PrettyMIDI('untitled.mid')

# Set is_drum=True for each instrument in the loaded MIDI data
for instrument in midi_data.instruments:
    instrument.is_drum = True

# Write the modified MIDI data back to the original file or a new file
midi_data.write('modified_untitled.mid')

# Create a dictionary to store notes by pitch
notes_by_pitch = {}

# Store notes above 51 to keep them in every file
notes_above_51 = []

# Iterate through instrument notes and group by pitch
for instrument in midi_data.instruments:
    for note in instrument.notes:
        if note.pitch > 51:
            # Modify the duration to be a quarter note
            
            notes_above_51.append(note)
        if note.pitch not in notes_by_pitch:
            notes_by_pitch[note.pitch] = []
        notes_by_pitch[note.pitch].append(note)

# Combine D2 and E2 notes in the same list
notes_by_pitch[38].extend(notes_by_pitch[40])
notes_by_pitch[40] = []

# Create output directory
output_directory = 'output_directory'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

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