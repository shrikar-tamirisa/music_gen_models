import os
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt

def quantize_note_length(note_length, quantization_level):
    """Quantizes note length to a discrete category based on quantization level.

    Args:
        note_length (float): Note length in quarter notes.
        quantization_level (int): Number of quantization levels.

    Returns:
        int: Quantized note length category (0 to quantization_level-1).
    """
    quantized_index = int(note_length * quantization_level)
    return min(quantized_index, quantization_level - 1) 

def calculate_note_length_transition_matrix(midi_file, quantization_level=8):
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    note_lengths = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note_lengths.append(note.end - note.start)  # Length in seconds

    quantized_lengths = [quantize_note_length(length, quantization_level) 
                         for length in note_lengths]

    transition_matrix = np.zeros((quantization_level, quantization_level))
    for i in range(len(quantized_lengths) - 1):
        prev_length = quantized_lengths[i]
        current_length = quantized_lengths[i + 1]
        transition_matrix[prev_length, current_length] += 1

    return transition_matrix

def calculate_average_transition_matrix(folder_path, quantization_level=8):
    total_matrix = np.zeros((quantization_level, quantization_level))
    num_files = 0

    for filename in os.listdir(folder_path):
        if filename.endswith('.mid'):
            file_path = os.path.join(folder_path, filename)
            transition_matrix = calculate_note_length_transition_matrix(file_path, quantization_level)
            total_matrix += transition_matrix
            num_files += 1

    if num_files > 0:
        return total_matrix / num_files
    else:
        print("No MIDI files found in the specified folder.")
        return None

def display_transition_matrix(matrix):
    plt.imshow(matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.xlabel('Current Quantized Note Length')
    plt.ylabel('Previous Quantized Note Length')
    plt.title('Note Length Transition Matrix')
    plt.show()

# --- Example Usage ---
folder_path = r"D:\Music-GAN\Generate_Your_Own_Music-main\rnwgan_gen_dataset"  # Replace with your folder path
quantization_level = 8  # Adjust for desired granularity

average_matrix = calculate_average_transition_matrix(folder_path, quantization_level)

if average_matrix is not None:
    display_transition_matrix(average_matrix) 
