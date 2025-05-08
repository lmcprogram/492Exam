#!/usr/bin/env python3

import sys
from typing import Dict, List, Tuple

def read_fasta(filename: str):
    """
    We read a FASTA file and returns the DNA sequence as a single uppercase string,
    ignoring any header lines (starting at line starting with A,C,G,T).

    Arguments:
        a filename as a string that is the path to the FASTA file.

    Returns:
        a string of the concatenated uppercase DNA sequence for simplicity.
    """
    dna_sequence = []
    # Open the file and read it line by line
    with open(filename, 'r') as fasta_file:
        for line in fasta_file:
            # Remove leading and trailing whitespace
            line = line.strip()
            # check if empty line or non-DNA character line
            if not line or not (line.upper().startswith('A') or line.upper().startswith('C') or line.upper().startswith('G') or line.upper().startswith('T')):
                continue  # Skip the line if it is, append the line to the list otherwise
            dna_sequence.append(line.upper())
    return ''.join(dna_sequence) #string


def extract_kmers(sequence: str, k: int):
    """
    We extract all the k-mers and the character (ACGT) following them for later analysis.

    Arguments:
        a sequence as a string with the DNA sequence.
        k (int): Length of the k-mer.

    Returns:
        a dict[str, list[str]] which is a dictionary of each k-mer and its following character.
    """
    kmers = {}
    # Loop through the sequence to extract k-mers and their following characters
    for i in range(len(sequence) - k):
        kmer = sequence[i:i + k]
        next_char = sequence[i + k]
        # Check if the k-mer is already in the dictionary
        if kmer in kmers:
            kmers[kmer].append(next_char) # append the next character to the list
        else:
            kmers[kmer] = [next_char] # create a new entry with the next character in a list
    return kmers  # return format: Dict[str, List[str]]


def count_frequencies(kmer_contexts: Dict[str, List[str]]):
    """
    we count the total frequency of each k-mer sequence and its subsequent characters frequency as well.

    Arguments:
        kmer_contexts (dict) which is a dictionary of each k-mer and its following character. (from extract_kmers)

    Returns:
        a dict[str, tuple[int, dict[str, int]]]:
        A dictionary where each k-mer is mapped to its total count with another dictionary showing how frequently each character follows that k-mer.
        (Yes I know this is overcomplicated and sloppy but it works!)
    """
    result = {}
    # Loop through the k-mer contexts to count frequencies
    for kmer, follows in kmer_contexts.items():
        total = len(follows)
        follow_counts = {}
        # Count the frequency of each character following
        for char in follows:
            if char in follow_counts:
                follow_counts[char] += 1
            else:
                follow_counts[char] = 1
        result[kmer] = (total, follow_counts)

    #print(result)
    return result  #return format: Dict[str, Tuple[int, Dict[str, int]]]

def write_output(kmer_counts: Dict[str, Tuple[int, Dict[str, int]]], out_file: str):
    """
    In this function we write the k-mer counts to the output file.

    Arguments:
        a dictionary of kmer_counts which is the mapping of k-mers to counts and following-character frequencies.
        a out_file as a string with the path (and name) to the output file.

    Returns:
        nothing but a message saying the file was written! (yay)
    """
    # Open the output file for writing
    with open(out_file, 'w') as f:
        #loop through a sorted version of the kmer_counts dictionary and write the k-mer, total count, and frequency of next character to the file
        for kmer in sorted(kmer_counts):
            total, follow_dict = kmer_counts[kmer]
            follow_str = ", ".join(f"{char}: {count}" for char, count in follow_dict.items())
            f.write(f"{kmer}: {total}, frequency of next character: {{{follow_str}}}\n")
    # sucess statement
    print(f"Output written to {out_file} sucessfully!")
    return 0 # I like returning 0 in functions even if it is not necessary just for future reference.

def main():
    """
    the main function is used to parse command-line arguments and process the input file.
    comments explain each part of the main function.
    """
    # Check if the correct number of input arguments is provided by a user, letting them know how to use the script if not.
    if len(sys.argv) != 4:
        print("How to use: python kmer_analysis.py <input_file> <output_file> <k>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    k = sys.argv[3]

    # Check if the input k is a positive integer
    try:
        k = int(sys.argv[3])
    except ValueError:
        print("Error: k must be an integer.") #otherwise prompt the user to enter a valid integer
        sys.exit(1)

    #check if k is usable (0 or negative will not work)
    if k <= 0:
        print("Error: k must be an integer greater than 0") #otherwise prompt the user to enter a valid integer
        sys.exit(1)

    # run all the subfunctions in order to read the input file, extract k-mers, count frequencies, and write the output
    sequence = read_fasta(input_file)
    kmer_contexts = extract_kmers(sequence, k)
    kmer_counts = count_frequencies(kmer_contexts)
    write_output(kmer_counts, output_file)


if __name__ == "__main__":
    main()
