import os
import re
from collections import defaultdict
from mido import MidiFile, MidiTrack

def concatenate_staff_segments(directory):
    # Pattern to match files named staff_segment_*.mid
    pattern = re.compile(r'staff_segment_(\d+)\.mid$')

    # Traverse directory and subdirectories
    for subdir, dirs, files in os.walk(directory):
        if "segmentation" in subdir.split(os.path.sep):
            # Group files by the "segmentation" directory
            files_grouped = defaultdict(list)
            for filename in files:
                match = pattern.match(filename)
                if match:
                    mvt_number = match.group(1)
                    files_grouped[subdir].append((int(mvt_number), os.path.join(subdir, filename)))

            # Process each group
            for segmentation_dir, files in files_grouped.items():
                # Sort files by segment number
                sorted_files = sorted(files, key=lambda x: x[0])
                midi_tracks = []

                for _, filepath in sorted_files:
                    midi = MidiFile(filepath)
                    midi_tracks.extend(midi.tracks)

                # Create new MIDI file
                new_midi = MidiFile()
                new_track = MidiTrack()
                new_midi.tracks.append(new_track)

                # Concatenate all tracks
                for track in midi_tracks:
                    for msg in track:
                        new_track.append(msg)

                # Determine the name based on the directory two levels up from the 'segmentation' directory
                grandparent_dir_name = os.path.basename(os.path.normpath(os.path.join(segmentation_dir, "..")))
                output_filename = f"{grandparent_dir_name}.mid"
                output_path = os.path.join(os.path.join(segmentation_dir, "../.."), output_filename)
                new_midi.save(output_path)
                print(f"Saved concatenated file: {output_path}")

# Call the function with the target directory containing "outputs/*/segmentation/"
concatenate_staff_segments("outputs")
