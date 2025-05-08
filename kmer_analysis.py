#!/usr/bin/env python3

import sys
from collections import defaultdict
from typing import Dict, List, Tuple

def read_fasta(filename: str):
    dna_sequence = []
    with open(filename, 'r') as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line or line.startswith('>'):
                continue  # Skip empty lines and headers
            dna_sequence.append(line.upper())
    return ''.join(dna_sequence) #string


def extract_kmers(sequence: str, k: int):
    kmers = defaultdict(list)
    for i in range(len(sequence) - k):
        kmer = sequence[i:i + k]
        next_char = sequence[i + k]
        kmers[kmer].append(next_char)
    return kmers # return format: Dict[str, List[str]]

def count_frequencies(kmer_contexts: Dict[str, List[str]]):
    result = {}
    for kmer, follows in kmer_contexts.items():
        total = len(follows)
        follow_counts = {}
        for char in follows:
            if char in follow_counts:
                follow_counts[char] += 1
            else:
                follow_counts[char] = 1
        result[kmer] = (total, follow_counts)

    #print(result)
    return result  #return format: Dict[str, Tuple[int, Dict[str, int]]]

def write_output(kmer_counts: Dict[str, Tuple[int, Dict[str, int]]], out_file: str):
    with open(out_file, 'w') as f:
        for kmer in sorted(kmer_counts):
            total, follow_dict = kmer_counts[kmer]
            follow_str = ", ".join(f"{char}: {count}" for char, count in follow_dict.items())
            f.write(f"{kmer}: {total}, frequency of next character: {{{follow_str}}}\n")
    return 0

def main():
    if len(sys.argv) != 4:
        print("How to use: python kmer_analysis.py <input_file> <output_file> <k>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    k = sys.argv[3]
    if not isinstance(k, int):
        print("Error: k must be an integer greater than 0")
        sys.exit(1)
    if k <= 0:
        print("Error: k must be an integer greater than 0")
        sys.exit(1)
    k = int(k)
    
    sequence = read_fasta(input_file)
    kmer_contexts = extract_kmers(sequence, k)
    kmer_counts = count_frequencies(kmer_contexts)
    write_output(kmer_counts, output_file)


if __name__ == "__main__":
    main()
