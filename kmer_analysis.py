import sys
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

def read_fasta(filename: str) -> str:
    sequence = []
    with open(filename, 'r') as file:
        for line in file:
            if not line.startswith('>'):
                sequence.append(line.strip().upper())
    return ''.join(sequence)

def main():
    if len(sys.argv) != 4:
        print("Usage: python kmer_analysis.py <input_file> <output_file> <k>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        k = int(sys.argv[3])
    except ValueError:
        print("Error: k must be an integer.")
        sys.exit(1)

    sequence = read_fasta(input_file)

if __name__ == "__main__":
    main()
