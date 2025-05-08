import sys
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

def read_fasta(filename: str):
    dna_sequence = []
    with open(filename, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line or line.startswith('>'):
                continue  # Skip empty lines and headers
            dna_sequence.append(line.upper())
    return ''.join(dna_sequence) #str


def extract_kmers(sequence: str, k: int):
    kmers = defaultdict(list)
    for i in range(len(sequence) - k):
        kmer = sequence[i:i + k]
        next_char = sequence[i + k]
        kmers[kmer].append(next_char)
    return kmers # Dict[str, List[str]]

def main():
    if len(sys.argv) != 4:
        print("How to use: python kmer_analysis.py <input_file> <output_file> <k>")
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
