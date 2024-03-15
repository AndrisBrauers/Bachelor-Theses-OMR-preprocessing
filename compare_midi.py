import mido
import editdistance
from difflib import SequenceMatcher
import os
from strsimpy.damerau import Damerau
        
def manhattan_distance(list1, list2):
    distance = 0
    for sub1, sub2 in zip(list1, list2):
        sub_distance = 0
        for x, y in zip(sub1, sub2):
            sub_distance += abs(x - y)
        distance += sub_distance
    return distance

def compare_midi_files2(file1, file2):
    # Read the content of each MIDI file in binary mode
    with open(file1, 'rb') as f:
        content1 = f.read()
    with open(file2, 'rb') as f2:
        content2 = f2.read()
    
    # Convert binary content to hexadecimal for comparison
    hex_content1 = content1.hex()
    hex_content2 = content2.hex()
    
    # Calculate similarity ratio
    damerau = Damerau()
    similarity_distance = damerau.distance(hex_content1, hex_content2)
    return  similarity_distance
    # # Load midi files
    # mid1 = mido.MidiFile(file1)
    # mid2 = mido.MidiFile(file2)

    # # Extract notes from midi files and group adjacent pitches together
    # notes1 = []
    # for msg in mido.merge_tracks(mid1.tracks):
    #     if 'note_on' in msg.type:
    #         pitch = msg.note
    #         if notes1 and pitch == notes1[-1][-1] + 1:
    #             # Append pitch to last group
    #             notes1[-1].append(pitch)
    #         else:
    #             # Create new group for pitch
    #             notes1.append([pitch])

    # notes2 = []
    # for msg in mido.merge_tracks(mid2.tracks):
    #     if 'note_on' in msg.type:
    #         pitch = msg.note
    #         if notes2 and pitch == notes2[-1][-1] + 1:
    #             # Append pitch to last group
    #             notes2[-1].append(pitch)
    #         else:
    #             # Create new group for pitch
    #             notes2.append([pitch])

    # # Calculate similarity for each group of pitches
    # similarity_scores = []
    # return manhattan_distance(notes1, notes2)



def text_file_compare(file1, file2):
    # Read the content of each MIDI file in binary mode
    with open(file1, 'rb') as f:
        content1 = f.read()
    with open(file2, 'rb') as f2:
        content2 = f2.read()
    
    # Convert binary content to hexadecimal for comparison
    hex_content1 = content1.hex()
    hex_content2 = content2.hex()
    
    # Calculate similarity ratio
    m = SequenceMatcher(None, hex_content1, hex_content2)
    return m.ratio()

def compare_directories(base_dir, output_dir, result_file_pitch, result_file_binary):
    # Open the result file for writing
    with (open(result_file_pitch, 'w') as result_pitch,
          open(result_file_binary, 'w') as result_binary):
        # Walk through the output directory structure
        for subdir, dirs, files in os.walk(output_dir):
            for filename in files:
                if ".mid" in filename:
                    base_file_path = os.path.join(base_dir, filename)
                    output_file_path = os.path.join(subdir, filename)
                    
                    # Check if the matching file exists in the base directory
                    if os.path.exists(base_file_path):
                        # Compare the files and get the similarity ratio
                        # similarity_binary = text_file_compare(base_file_path, output_file_path)
                        similarity_pitch = compare_midi_files2(base_file_path, output_file_path)
                        
                        # Write the comparison result to the result file
                        result_pitch.write(f"{output_file_path}: {similarity_pitch}\n")
                        #result_binary.write(f"{output_file_path}: {similarity_binary}\n")
                    else:
                        # If the matching file does not exist in the base directory, write a note
                        result_pitch.write(f"{output_file_path}: No matching file in base directory\n")
                        #result_binary.write(f"{output_file_path}: No matching file in base directory\n")

# Directories to compare
base_dir = 'audiveris/outputs/nonprocessed/segmentation'
output_dir = 'audiveris/outputs'

# Result file path
result_file_pitch = 'comparison_results_pitch.txt'
result_file_binary = 'comparison_results_binary.txt'

# Run the comparison
compare_directories(base_dir, output_dir, result_file_pitch, result_file_binary)
#print(similarity) # higher it is, the less similar files are

#https://stackoverflow.com/questions/74301750/python-compare-midi-files