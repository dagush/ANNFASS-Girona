from difflib import SequenceMatcher
import jellyfish

def similarSM(a, b):
    return SequenceMatcher(None, a, b).ratio()

def similarLevenshtein(a, b):
    return jellyfish.levenshtein_distance(a,b)

def similarJaro(a,b):
    return jellyfish.jaro_distance(a,b)

def similarDamerau(a,b):
    return jellyfish.damerau_levenshtein_distance(a,b)

def similarHamming(a,b):
    return jellyfish.hamming_distance(a, b)
