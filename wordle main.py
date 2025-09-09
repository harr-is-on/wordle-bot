# wordle_runtime_auto.py (TXT version)
# Interactive solver that always follows the suggested word.
# Round 1 uses fixed opening "soare" and asks for 012 feedback.
# Round 2 uses the precomputed lookup CSV (fallback to presence-based suggestion if missing).
# Round 3+ uses presence-based suggestions over the current candidate set.

import re, csv, collections
from typing import List, Optional, Dict

TXT_PATH = "wordle database 3189.txt"       # your dictionary TXT (same folder)
LOOKUP_CSV = "soare_first_pattern_to_best_second.csv"
OPENING = "soare"

def load_words_from_txt(path: str) -> List[str]:
    words = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = re.sub(r"[^A-Za-z]", "", line.strip()).lower()
            if len(w) == 5:
                words.append(w)
    words = sorted(set(words))
    if not words:
        raise RuntimeError("No 5-letter words found in TXT.")
    return words

def pattern_012(guess: str, answer: str) -> str:
    res = [0]*5
    cnt = collections.Counter(answer)
    # greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            res[i] = 2
            cnt[g] -= 1
    # yellows / grays
    for i, g in enumerate(guess):
        if res[i] == 0:
            if cnt[g] > 0:
                res[i] = 1
                cnt[g] -= 1
            else:
                res[i] = 0
    return "".join(str(x) for x in res)

def filter_candidates(cands: List[str], guess: str, pat: str) -> List[str]:
    return [w for w in cands if pattern_012(guess, w) == pat]

def letter_presence_freq(words: List[str]):
    n = len(words)
    cnt = {ch: 0 for ch in "abcdefghijklmnopqrstuvwxyz"}
    for w in words:
        for ch in set(w):
            cnt[ch] += 1
    return {ch: cnt[ch]/n for ch in cnt}

def suggest_by_presence(cands: List[str]) -> str:
    pres = letter_presence_freq(cands)
    def score(w: str) -> float:
        return sum(pres.get(ch, 0.0) for ch in set(w))
    # Ties: prefer more unique letters, then lexicographically smaller word
    return max(cands, key=lambda w: (score(w), len(set(w)), w))

def load_second_move_lookup(csv_path: str) -> Dict[str, str]:
    table: Dict[str, str] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            table[row["pattern"]] = row["best_g2"]
    return table

def main():
    words = load_words_from_txt(TXT_PATH)
    candidates = words[:]
    try:
        second_lookup = load_second_move_lookup(LOOKUP_CSV)
    except Exception:
        second_lookup = {}

    print(f"Opening word: {OPENING}")
    pat1 = input("[Round 1] Enter feedback for 'soare' (e.g., 02201; 0=gray,1=yellow,2=green): ").strip()
    if not re.fullmatch(r"[012]{5}", pat1):
        print("Invalid input. Please enter exactly 5 digits of 0/1/2.")
        return

    candidates = filter_candidates(candidates, OPENING, pat1)
    print(f"Remaining candidates: {len(candidates)}")
    if pat1 == "22222":
        print("Solved.")
        return
    if not candidates:
        print("No matching candidates. Check your word list or feedback.")
        return

    guess = second_lookup.get(pat1) or suggest_by_presence(candidates)
    round_idx = 2

    while True:
        print(f"[Round {round_idx}] Using suggestion: {guess}")
        pat = input(f"[Round {round_idx}] Enter feedback (e.g., 02201; 0=gray,1=yellow,2=green): ").strip()
        if not re.fullmatch(r"[012]{5}", pat):
            print("Invalid input. Please enter exactly 5 digits of 0/1/2.")
            continue

        candidates = filter_candidates(candidates, guess, pat)
        print(f"Remaining candidates: {len(candidates)}")

        if pat == "22222":
            print("Solved.")
            break
        if not candidates:
            print("No matching candidates. Check your word list or feedback.")
            break

        round_idx += 1
        guess = suggest_by_presence(candidates)
        if round_idx > 10:
            print("Exceeded 10 rounds. Stopping.")
            break

if __name__ == "__main__":
    main()
