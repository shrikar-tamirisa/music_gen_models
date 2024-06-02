import os
from music21 import converter

def convert_krn_to_mid(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all .krn files in the input folder
    krn_files = [file for file in os.listdir(input_folder) if file.endswith(".krn")]

    for krn_file in krn_files:
        # Construct input and output file paths
        input_file_path = os.path.join(input_folder, krn_file)
        output_file_path = os.path.join(output_folder, os.path.splitext(krn_file)[0] + ".mid")

        try:
            # Convert .krn to .mid using music21
            score = converter.parse(input_file_path)
            score.write('midi', fp=output_file_path)
            print(f"Conversion successful: {krn_file} -> {os.path.basename(output_file_path)}")
        except Exception as e:
            print(f"Error converting {krn_file}: {str(e)}")

if __name__ == "__main__":
    # Specify source and destination folders
    source_folder = r"D:\Music-GAN\Mozart1\mozart-piano-sonatas-main\kern"
    destination_folder = r"D:\Music-GAN\Mozart"

    # Convert .krn to .mid
    convert_krn_to_mid(source_folder, destination_folder)
