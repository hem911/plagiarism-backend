import re

def split_into_chunks(text, size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)

    return chunks[:10]

def calculate_similarity(text1, text2):
    w1 = clean(text1).split()
    w2 = clean(text2).split()

    set1 = set(make_ngrams(w1))
    set2 = set(make_ngrams(w2))

    if not set1 or not set2:
        return 0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    score = (intersection / union) * 100
    return round(score)

def make_ngrams(words, n=3):
    return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]

def clean(text):
    text = text.lower()
    return re.sub(r"[^a-z0-9\s]", "", text)
