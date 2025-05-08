# kmer_analysis.py

A command-line Python script that is used for analyzing k-mers (substrings of length *k*) in DNA sequences from FASTA files. It can extract all k-mers, recording the frequency of the character that follows it, with the output being saved to a file.
## What can it do?

- Read DNA sequences from the FASTA file format (ignoring non-DNA starting lines and headers).
- Extract all k-mers of user-input length in the commandline, tracking the following characters.
- Count frequency of every k-mer and their next-character frequency too.
- Outputs results in a readable file sorted alphabetically by k-mer.
- Includes a `pytest` test suite covering typical and edge case functionalities.

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

## Output Format (based on the example usage)

```
AAA: 1, frequency of next character: {C: 1, G: 3}
AAC: 1, frequency of next character: {T: 2}
```
and so on

## How to test

- The suite of tests can be run using pytest in the following way
```bash
pytest test_kmer_analysis.py
```

- The suite tests each function and verifies they operate as expected.

##
This repo was made for Exam 4 in BIO/DSP 439/539!

Thank you for the great semester and have a great summer Professor Schwartz!