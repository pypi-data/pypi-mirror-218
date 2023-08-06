import os
import argparse
from gpx_concatenator.gpx_concatenator import GPXConcatenator

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='GPX Concatenator')
    parser.add_argument('--input-dir', default='input', help='Directory containing input files')
    parser.add_argument('--output-file', default='output.gpx', help='Output file name')
    parser.add_argument('--enable-metadata', action='store_true', help='Enable metadata in the output file')
    parser.add_argument('--enable-coloring', action='store_true', help='Enable coloring in the output file')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the input files from the specified directory
    input_files = sorted([os.path.join(args.input_dir, file) for file in os.listdir(args.input_dir) if file.endswith('.gpx')])

    # Create an instance of GPXConcatenator with the specified parameters
    concatenator = GPXConcatenator(
        input_files,
        args.output_file,
        enable_metadata=args.enable_metadata,
        enable_coloring=args.enable_coloring
    )

    # Concatenate the files
    concatenator.concatenate_files()

if __name__ == '__main__':
    main()
