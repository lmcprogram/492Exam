# test_kmer_analysis.py

import tempfile
import os
import pytest
from kmer_analysis import read_fasta, extract_kmers, count_frequencies, write_output


def test_read_fasta():
    # Setup
    content = ">header\nACTG\nCGA\n"
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    # Execute
    sequence = read_fasta(tmp_path)

    # Cleanup
    os.remove(tmp_path)

    # Verify
    assert sequence == "ACTGCGA"

def test_extract_kmers_normal_input():
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

def test_extract_kmers_edge_too_short():
    sequence = "AT"
    k = 3
    result = extract_kmers(sequence, k)
    assert result == {}  # should have no k-mers if k > len(sequence)

def test_count_kmer_frequencies_typical():
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


def test_write_output(tmp_path):
    # Setup data
    kmer_data = {
        "AT": (2, {"G": 2}),
        "TG": (1, {"A": 1})
    }
    expected_lines = {
        'TG: 1, frequency of next character: {A: 1}\n',
        'AT: 2, frequency of next character: {G: 2}\n'
    }

    # Run
    output_file = tmp_path / "output.txt"
    write_output(kmer_data, str(output_file))

    # Verify
    with open(output_file, 'r') as f:
        lines = set(f.readlines())
        assert lines == expected_lines
