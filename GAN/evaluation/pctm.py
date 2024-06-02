import os
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt

def calculate_pitch_class_transition_matrix(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    pitches = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitches.append(note.pitch)

    pitch_classes = [pitch % 12 for pitch in pitches]

    transition_matrix = np.zeros((12, 12))
    for i in range(len(pitch_classes) - 1):
        prev_class = pitch_classes[i]
        current_class = pitch_classes[i + 1]
        transition_matrix[prev_class, current_class] += 1

    return transition_matrix

def calculate_average_transition_matrix(folder_path):
    """
    Calculates the average pitch class transition matrix from all MIDI files in a folder.

    Args:
        folder_path (str): Path to the folder containing MIDI files.

    Returns:
        numpy.ndarray: Average pitch class transition matrix.
    """
    total_matrix = np.zeros((12, 12))
    num_files = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.mid'):
            file_path = os.path.join(folder_path, filename)
            transition_matrix = calculate_pitch_class_transition_matrix(file_path)
            total_matrix += transition_matrix
            num_files += 1

    # Check if any files were found
    if num_files > 0:
        return total_matrix / num_files
    else:
        print("No MIDI files found in the specified folder.")
        return None

def display_transition_matrix(matrix):
    plt.imshow(matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.xlabel('Current Pitch Class')
    plt.ylabel('Previous Pitch Class')
    plt.title('Average Pitch Class Transition Matrix')
    plt.show()

# --- Example Usage ---
folder_path = r"D:\Music-GAN\Generate_Your_Own_Music-main\rnwgan_gen_dataset"  # Replace with your folder path
average_matrix = calculate_average_transition_matrix(folder_path)

if average_matrix is not None:
    display_transition_matrix(average_matrix)
