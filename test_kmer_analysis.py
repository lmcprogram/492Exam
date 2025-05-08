# test_kmer_analysis.py

import tempfile
import os
import pytest
from kmer_analysis import read_fasta, extract_kmers, count_frequencies, write_output


# Testing of the input function

def test_read_fasta():
    """Tests reading a basic FASTA file with a header and sequence lines."""
    # Setup temporary FASTA file
    content = ">header\nACTG\nCGA\n"
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Execute function
    sequence = read_fasta(tmp_path)

    # Cleanup temp file
    os.remove(tmp_path)

    # Verify expected sequence
    assert sequence == "ACTGCGA"


def test_read_fasta_lowercase():
    """Tests that lowercase DNA input is correctly converted to uppercase."""
    # Lowercase sequence input
    content = "acgt\ntgca\n"
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Execute and cleanup
    result = read_fasta(tmp_path)
    os.remove(tmp_path)

    # Verify uppercase output
    assert result == "ACGTTGCA"

def test_read_fasta_non_dna_lines():
    """Tests that non-DNA lines are ignored."""
    # Mixed content input
    content = ">description\n123\nACGT\n!!!\nTGCA\n"
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Execute and cleanup
    result = read_fasta(tmp_path)
    os.remove(tmp_path)

    # Verify DNA-only result
    assert result == "ACGTTGCA"


# Testing of the kmer extraction function

def test_extract_kmers_normal_input():
    """Tests the extraction of k-mers from a normal DNA sequence."""
    # k=2 normal input
    sequence = "ATGCGA"
    k = 2
    expected = {
        "AT": ["G"],
        "TG": ["C"],
        "GC": ["G"],
        "CG": ["A"]
    }
    result = extract_kmers(sequence, k)
    assert result == expected

def test_extract_kmers_k_equals_1():
    """Tests the extraction of k-mers with k=1."""
    # k=1 (single base prefixes)
    sequence = "ACGT"
    k = 1
    expected = {
        "A": ["C"],
        "C": ["G"],
        "G": ["T"]
    }
    result = extract_kmers(sequence, k)
    assert result == expected

def test_extract_kmers_edge_too_short():
    """Tests the extraction of k-mers from a sequence that is too short."""
    # k longer than sequence
    sequence = "AT"
    k = 3
    result = extract_kmers(sequence, k)
    assert result == {}

def test_extract_kmers_overlap():
    """Tests the extraction of overlapping k-mers."""
    # overlapping repeating k-mers
    sequence = "AAAAA"
    k = 2
    expected = {
        "AA": ["A", "A", "A"]
    }
    result = extract_kmers(sequence, k)
    assert result == expected

def test_extract_kmers_empty_sequence():
    """Tests the extraction of k-mers from an empty sequence."""
    # empty input
    assert extract_kmers("", 3) == {}

def test_extract_kmers_k_equals_len():
    """Tests the extraction of k-mers where k equals the length of the sequence."""
    # k == len(sequence), no next char
    sequence = "ACGT"
    assert extract_kmers(sequence, 4) == {}


# Testing of the frequency counting function

def test_count_frequencies_empty_input():
    """Tests the frequency counting function with empty input."""
    # no kmers to count
    result = count_frequencies({})
    assert result == {}

def test_count_frequencies_balanced_following():
    """Tests the frequency counting function with balanced following characters."""
    # two types of next chars, equal frequency
    input_data = {
        "AC": ["G", "T", "G", "T"]
    }
    expected = {
        "AC": (4, {"G": 2, "T": 2})
    }
    assert count_frequencies(input_data) == expected

def test_count_frequencies_shared_following():
    """Tests the frequency counting function with shared following characters."""
    # different k-mers with same following char
    input_data = {
        "AC": ["T"],
        "GT": ["T"]
    }
    expected = {
        "AC": (1, {"T": 1}),
        "GT": (1, {"T": 1})
    }
    assert count_frequencies(input_data) == expected

def test_count_kmer_frequencies_typical():
    """Tests the frequency counting function with typical input."""
    # typical k-mer frequency mix
    kmer_contexts = {
        "AT": ["G", "G", "C"],
        "TG": ["A"]
    }
    expected = {
        "AT": (3, {"G": 2, "C": 1}),
        "TG": (1, {"A": 1})
    }
    result = count_frequencies(kmer_contexts)
    assert result == expected

def test_count_frequencies_single_kmer():
    """Tests the frequency counting function with a single k-mer."""
    # one k-mer and one next char
    input_data = {
        "GG": ["C"]
    }
    expected = {
        "GG": (1, {"C": 1})
    }
    assert count_frequencies(input_data) == expected


# Testing the output function

def test_write_output_sorting(tmp_path):
    """Tests the output function with sorting."""
    # test sorted k-mer output
    kmer_data = {
        "GT": (1, {"A": 1}),
        "AC": (2, {"T": 2})
    }
    expected = [
        'AC: 2, frequency of next character: {T: 2}\n',
        'GT: 1, frequency of next character: {A: 1}\n'
    ]

    output_file = tmp_path / "sorted_output.txt"
    write_output(kmer_data, str(output_file))

    # Verify output lines match expected order and format
    with open(output_file) as f:
        assert f.readlines() == expected


def test_write_output(tmp_path):
    """Tests the output function with a basic example."""
    # basic unsorted input test
    kmer_data = {
        "AT": (2, {"G": 2}),
        "TG": (1, {"A": 1})
    }
    expected_lines = {
        'TG: 1, frequency of next character: {A: 1}\n',
        'AT: 2, frequency of next character: {G: 2}\n'
    }

    # Write and verify unordered output
    output_file = tmp_path / "output.txt"
    write_output(kmer_data, str(output_file))

    with open(output_file, 'r') as f:
        lines = set(f.readlines())
        assert lines == expected_lines
