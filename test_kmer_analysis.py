# test_kmer_analysis.py

import tempfile
import os
import pytest
from kmer_analysis import read_fasta, extract_kmers


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

def test_extract_kmers_typical():
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
