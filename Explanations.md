# Data Structures used for k-mers
## List
- briefly a list is used store DNA Sequences before they are iterated over and placed into the dictionary.
- a list is then used to embed into the dictionary before being converting into a dictionary for the final output.  (more explanation in code AND below) 

## Dict (Dictionary)
- a dictionary was used in:
     - ``` extract_kmers() ```
     - ``` count_frequencies() ```
     - ``` write_output() ```
- I used a dictionary to store all the k-mers along side their following characters.  It allows for a easy traversal and testing since we are effectively making a "term" (the k-mer in question) and the "definition" (the frequency).  That can be combined to make the "definition" represent the frequency AND the following characters AND their subsequent frequencies using a different data structure (Tuple).  I like using dictionaries because they make inputs faster and easier to search for when compared to the jumbled complex mess of vectors or trying to use pairs of pairs etc.

## Tuples
- a tuple is data structure that can store more than one item into a single variable, kind of like a pair but with more flexibility.
- a Tuple was used in:
    - ```count_frequencies()```
    - ``` write_output() ```
- the Tuple was used in conjunction with the dictionary, which transformed from a ```Dict[str, List[str]]``` (after being returned from ```extract_kmers()```) being translated into this new dictionary:
    - ```Dict[str, Tuple[int, Dict[str, int]]]```
    - which stored the
        - k-mer as the first string
        - a Tuple with the frequency now linked to another dictionary!  
        This new dictionary was then used much like the first to store:
            - the character the follows as a string
            - and its respective frequency of appearance (int)!
##
Is this needlessly complex, yeah probably.  I could've used dataframes or possibly even just pairs like a I said before.  I could've even used sepearte vectors sorted to match kmers and next values and then print them in a csv format, but with these dictionaries and tuples I was able to make the script run very quick and stable (unlike my incredibly slow bash script from Exam 2).

# Handling of Edge Cases

- so for edge cases like the first and last k-mer in a sequence, I handled them in my ```test_kmer_analysis.py``` using pytest. 
- My extract_kmers() function is forced to only include k-mers that have a following character, so the final k-mer is naturally excluded if it reaches the end of the sequence. 

- This behavior is tested in ```test_extract_kmers_k_equals_len()``` to ensure its functioning properly.  

- More so, I tested for other edge cases such as sequences shorter than k and empty input, both of which return an empty dictionary without errors.

- For the first k-mer in a sequence, my code similarly doesn't even read lines that don't include DNA sequences.  I was able to do this by checking in  ```read_fasta()``` after whitespace from the beginning and end is removed is the line is empty or doesn't start with a DNA character (ACGT), lowercase or uppercase.  All the tests in the suite also test for k values too large for the found sequence, and as stated before, everything passes.

- Lastly, there are a ton of tests.  Some I wrote, some ChatGPT helped with, and it led to many bugs being found through testing.  I fixed those and it kept leading to different possible tests.  I tried to include as many I could think of.  As a result I think the test suite is decently comprehensive.

# How do I avoid Over-Counting/Missing context

- as stated above, the ```read_fasta()``` function only operates when a valid sequence is found among every single line, ensuring now sequences are lost.  (Which also means that non DNA sequences can sneak in as well, oops.)

- AND my code avoids overcounting or missing context by carefully iterating over the sequence in ```extract_kmers()``` so that each k-mer is paired with EXACTLY one following character, if possible. 

- The loop stops at len(sequence) - k, ensuring we never attempt to access a character beyond the end of the string. This avoids both duplicated context and out-of-bounds errors. 

- Lastly, in ```count_frequencies()```, the following characters are counted using a dictionary that increments counts, so each occurrence is tallied only once The tests confirm that overlapping k-mers and shared following characters are counted correctly.

#

I think those answers are suffiencent.  Like I stated in the README, thank you for the great semester Professor!