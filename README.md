# kmer_analysis.py

A command-line Python tool for analyzing k-mers (substrings of length *k*) in DNA sequences from FASTA files. It extracts each k-mer and records the frequency of the nucleotide that follows it. Output is saved to a file for downstream analysis.

## Features

- Reads DNA sequences from FASTA format (ignoring non-DNA starting lines and headers).
- Extracts all k-mers of user-specified length and tracks following characters.
- Counts frequencies of each k-mer and its next-character occurrences.
- Outputs results in a human-readable format, sorted alphabetically by k-mer.
- Includes a `pytest` test suite covering all major functionalities.

## Requirements

- Python 3.6+
- `pytest` (for testing)

## Usage

```bash
python kmer_analysis.py <input_file> <output_file> <k>
```

- <input_file>: Path to the input FASTA file
- <output_file>: Path to write the results
- <k>: Integer length of the k-mers

Example: usage ``` python kmer_analysis.py sample.fa output.txt 3```

## Output Format